from datetime import UTC, datetime, timedelta
from enum import StrEnum

from PySide6.QtWidgets import QHBoxLayout, QLabel, QStackedWidget, QVBoxLayout, QWidget
from qfluentwidgets import SubtitleLabel, TitleLabel

from terminal.core.freshness import DataFreshness
from terminal.core.models import Candle
from terminal.ui.charts import MarketChartPanel
from terminal.ui.theme import SPACING_MEDIUM


class DashboardState(StrEnum):
    LOADING = "loading"
    READY = "ready"
    EMPTY = "empty"
    ERROR = "error"


class DashboardPage(QWidget):
    """Dashboard shell with explicit data lifecycle states."""

    def __init__(self) -> None:
        super().__init__()
        self._pages = QStackedWidget()
        self._state_pages = {
            DashboardState.LOADING: self._message_page(
                "로딩 중", "시장 데이터를 불러오고 있습니다."
            ),
            DashboardState.EMPTY: self._message_page(
                "표시할 데이터 없음", "활성화된 데이터 제공자가 없습니다."
            ),
            DashboardState.ERROR: self._message_page(
                "데이터 오류", "시장 데이터를 불러오지 못했습니다."
            ),
            DashboardState.READY: self._synthetic_page(),
        }
        for state in DashboardState:
            self._pages.addWidget(self._state_pages[state])
        layout = QVBoxLayout(self)
        layout.addWidget(self._pages)
        self.show_data()

    def show_loading(self) -> None:
        self._show(DashboardState.LOADING)

    def show_empty(self) -> None:
        self._show(DashboardState.EMPTY)

    def show_error(self) -> None:
        self._show(DashboardState.ERROR)

    def show_data(self) -> None:
        self._show(DashboardState.READY)

    def _show(self, state: DashboardState) -> None:
        self._pages.setCurrentWidget(self._state_pages[state])

    @staticmethod
    def _message_page(title: str, message: str) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addStretch()
        layout.addWidget(TitleLabel(title))
        layout.addWidget(SubtitleLabel(message))
        layout.addStretch()
        return page

    def _synthetic_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(TitleLabel("시장 대시보드"))
        layout.addWidget(SubtitleLabel("합성 데이터 · 과거 데이터 · 제공자: synthetic"))
        cards = QHBoxLayout()
        cards.setSpacing(SPACING_MEDIUM)
        for title, value in (
            ("KOSPI", "2,650.00"),
            ("S&P 500", "5,100.00"),
            ("USD/KRW", "1,350.00"),
        ):
            card = QWidget()
            card_layout = QVBoxLayout(card)
            card_layout.addWidget(QLabel(title))
            card_layout.addWidget(TitleLabel(value))
            cards.addWidget(card)
        layout.addLayout(cards)
        self._chart = MarketChartPanel()
        self._chart.setMinimumHeight(280)
        self._chart.symbol_changed.connect(self._refresh_chart)
        self._chart.timeframe_changed.connect(self._refresh_chart)
        self._refresh_chart()
        layout.addWidget(self._chart)
        layout.addStretch()
        return page

    def _refresh_chart(self) -> None:
        self._chart.set_candles(
            _synthetic_candles(
                self._chart.symbol.currentText(), self._chart.timeframe.currentText()
            )
        )


def _synthetic_candles(symbol: str, timeframe: str) -> list[Candle]:
    now = datetime.now(UTC).replace(second=0, microsecond=0)
    count = {"1D": 12, "1W": 20, "1M": 30, "1Y": 48}[timeframe]
    base_price = 180.0 if symbol == "NASDAQ:AAPL" else 70_000.0
    return [
        Candle(
            timestamp=now - timedelta(minutes=count - index),
            open=base_price + index * 0.2,
            high=base_price + 1.0 + index * 0.2,
            low=base_price - 0.5 + index * 0.2,
            close=base_price + 0.4 + index * 0.2,
            volume=1_000.0 + index * 25,
            provider="synthetic",
            freshness=DataFreshness.HISTORICAL,
        )
        for index in range(count)
    ]
