# ruff: noqa: E501

"""Chart widgets that consume normalized models, never provider payloads."""

import json
from collections.abc import Sequence
from datetime import UTC
from pathlib import Path

import pyqtgraph as pg  # type: ignore[import-untyped]
from PySide6.QtCore import QUrl, Signal
from PySide6.QtGui import QCloseEvent
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from terminal.core.freshness import DataFreshness
from terminal.core.models import Candle


class FreshnessBadge(QLabel):
    """Always exposes the provider's asserted freshness; it never infers LIVE."""

    def set_freshness(self, freshness: DataFreshness, delay_seconds: int | None = None) -> None:
        self.setText(freshness.label(delay_seconds))
        colors = {
            DataFreshness.LIVE: "#168c7a",
            DataFreshness.DELAYED: "#b87a12",
            DataFreshness.EOD: "#315b73",
            DataFreshness.HISTORICAL: "#315b73",
        }
        self.setStyleSheet(
            f"background: {colors[freshness]}; color: white; border-radius: 4px; padding: 3px 7px;"
        )


def candle_payload(candles: Sequence[Candle]) -> list[dict[str, float | int]]:
    """Convert UTC model values into the browser contract without raw API fields."""
    return [
        {
            "time": int(candle.timestamp.astimezone(UTC).timestamp()),
            "open": candle.open,
            "high": candle.high,
            "low": candle.low,
            "close": candle.close,
            "volume": candle.volume or 0.0,
        }
        for candle in sorted(candles, key=lambda item: item.timestamp)
    ]


_ASSET_DIRECTORY = Path(__file__).with_name("assets")
_CHART_HTML = """<!doctype html><html><body style='margin:0;background:#0c1e2d'>
<div id='chart' style='height:100vh;width:100vw'></div>
<script src='lightweight-charts.standalone.production.js'></script><script>
const host=document.getElementById('chart');
const chart=LightweightCharts.createChart(host,{layout:{background:{color:'#0c1e2d'},textColor:'#9ab4c6'},grid:{vertLines:{color:'#153348'},horzLines:{color:'#153348'}},rightPriceScale:{borderColor:'#23455d'},timeScale:{borderColor:'#23455d'}});
const candles=chart.addSeries(LightweightCharts.CandlestickSeries,{upColor:'#4ee0b1',downColor:'#ff7f9c',borderVisible:false,wickUpColor:'#4ee0b1',wickDownColor:'#ff7f9c'});
const volume=chart.addSeries(LightweightCharts.HistogramSeries,{priceFormat:{type:'volume'},priceScaleId:'volume'});volume.priceScale().applyOptions({scaleMargins:{top:.8,bottom:0}});
function setData(v){candles.setData(v);volume.setData(v.map(x=>({time:x.time,value:x.volume,color:x.close>=x.open?'#4ee0b188':'#ff7f9c88'})));chart.timeScale().fitContent()}
function update(v){candles.update(v);volume.update({time:v.time,value:v.volume,color:v.close>=v.open?'#4ee0b188':'#ff7f9c88'})}
window.setData=setData;window.update=update;new ResizeObserver(e=>chart.applyOptions({width:e[0].contentRect.width,height:e[0].contentRect.height})).observe(host);
</script></body></html>"""


class CandlestickChart(QWebEngineView):
    """QtWebEngine candlestick host with setData/update/dispose lifecycle methods."""

    loaded = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._disposed = False
        self._loaded = False
        self._pending: list[dict[str, float | int]] = []
        self.loadFinished.connect(self._on_load_finished)
        self.setHtml(_CHART_HTML, QUrl.fromLocalFile(f"{_ASSET_DIRECTORY}/"))

    def set_data(self, candles: Sequence[Candle]) -> None:
        self._pending = candle_payload(candles)
        self._run("setData", self._pending)

    def update_candle(self, candle: Candle) -> None:
        self._run("update", candle_payload((candle,))[0])

    def dispose(self) -> None:
        if not self._disposed:
            self._disposed = True
            self._loaded = False
            self.setHtml("", QUrl("about:blank"))

    def _on_load_finished(self, success: bool) -> None:
        if success:
            self._loaded = True
            if self._pending:
                self._run("setData", self._pending)
            self.loaded.emit()

    def _run(self, method: str, payload: object) -> None:
        if not self._disposed and self._loaded:
            self.page().runJavaScript(f"{method}({json.dumps(payload)})")


class YieldCurveChart(pg.PlotWidget):  # type: ignore[misc]
    """PyQtGraph curve for normalized yield values."""

    def set_curve(self, maturities: Sequence[float], yields: Sequence[float]) -> None:
        if len(maturities) != len(yields):
            raise ValueError("Maturities and yields must have the same length")
        self.clear()
        self.plot(list(maturities), list(yields), pen=pg.mkPen("#22d3ee", width=2), symbol="o")


class MarketChartPanel(QWidget):
    """Chart controls own only presentation state (symbol and timeframe)."""

    symbol_changed = Signal(str)
    timeframe_changed = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.symbol = QComboBox()
        self.symbol.addItems(("NASDAQ:AAPL", "KRX:005930"))
        self.timeframe = QComboBox()
        self.timeframe.addItems(("1D", "1W", "1M", "1Y"))
        self.freshness = FreshnessBadge()
        self.freshness.set_freshness(DataFreshness.HISTORICAL)
        self.chart = CandlestickChart()
        header = QHBoxLayout()
        header.setContentsMargins(12, 8, 12, 0)
        header.addWidget(QLabel("\ucc28\ud2b8"))
        header.addWidget(self.symbol)
        header.addWidget(self.timeframe)
        header.addWidget(self.freshness)
        header.addStretch()
        layout = QVBoxLayout(self)
        layout.addLayout(header)
        layout.addWidget(self.chart, 1)
        self.symbol.currentTextChanged.connect(self.symbol_changed)
        self.timeframe.currentTextChanged.connect(self.timeframe_changed)

    def set_candles(self, candles: Sequence[Candle]) -> None:
        self.chart.set_data(candles)
        if candles:
            self.freshness.set_freshness(candles[-1].freshness)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.chart.dispose()
        super().closeEvent(event)
