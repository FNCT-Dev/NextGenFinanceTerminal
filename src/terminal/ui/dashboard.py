# ruff: noqa: E501

from datetime import UTC, datetime, timedelta
from enum import StrEnum

from PySide6.QtWidgets import QGridLayout, QLabel, QStackedWidget, QVBoxLayout, QWidget
from qfluentwidgets import SubtitleLabel, TitleLabel

from terminal.core.freshness import DataFreshness
from terminal.core.models import Candle
from terminal.ui.charts import MarketChartPanel
from terminal.ui.theme import SPACING_LARGE, SPACING_MEDIUM, SPACING_SMALL


class DashboardState(StrEnum):
    LOADING = "loading"
    READY = "ready"
    EMPTY = "empty"
    ERROR = "error"


class MetricCard(QWidget):
    def __init__(self, title: str, value: str, change: str) -> None:
        super().__init__()
        self.setObjectName("metricCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING_MEDIUM, SPACING_MEDIUM, SPACING_MEDIUM, SPACING_MEDIUM)
        title_label = QLabel(title)
        title_label.setObjectName("muted")
        change_label = QLabel(change)
        change_label.setStyleSheet("color: #4ee0b1; font-weight: 600;")
        layout.addWidget(title_label)
        layout.addSpacing(SPACING_SMALL)
        layout.addWidget(TitleLabel(value))
        layout.addWidget(change_label)


class DashboardPage(QWidget):
    """Dashboard with explicit data states and a Glacial market workspace."""

    def __init__(self) -> None:
        super().__init__()
        self._pages = QStackedWidget()
        self._state_pages = {
            DashboardState.LOADING: self._message_page(
                "\ub85c\ub529 \uc911",
                "\uc2dc\uc7a5 \ub370\uc774\ud130\ub97c \ubd88\ub7ec\uc624\uace0 \uc788\uc2b5\ub2c8\ub2e4.",
            ),
            DashboardState.EMPTY: self._message_page(
                "\ud45c\uc2dc\ud560 \ub370\uc774\ud130 \uc5c6\uc74c",
                "\ud65c\uc131\ud654\ub41c \ub370\uc774\ud130 \uc81c\uacf5\uc790\uac00 \uc5c6\uc2b5\ub2c8\ub2e4.",
            ),
            DashboardState.ERROR: self._message_page(
                "\ub370\uc774\ud130 \uc624\ub958",
                "\uc2dc\uc7a5 \ub370\uc774\ud130\ub97c \ubd88\ub7ec\uc624\uc9c0 \ubabb\ud588\uc2b5\ub2c8\ub2e4.",
            ),
            DashboardState.READY: self._market_workspace(),
        }
        for state in DashboardState:
            self._pages.addWidget(self._state_pages[state])
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING_LARGE, SPACING_LARGE, SPACING_LARGE, SPACING_LARGE)
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
        page.setObjectName("surface")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(SPACING_LARGE, SPACING_LARGE, SPACING_LARGE, SPACING_LARGE)
        layout.addStretch()
        layout.addWidget(TitleLabel(title))
        text = SubtitleLabel(message)
        text.setObjectName("muted")
        layout.addWidget(text)
        layout.addStretch()
        return page

    def _market_workspace(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(SPACING_MEDIUM)
        layout.addWidget(TitleLabel("\uc2dc\uc7a5 \ub300\uc2dc\ubcf4\ub4dc"))
        summary = SubtitleLabel(
            "Synthetic \ub370\uc774\ud130 \uae30\ubc18 \uc2dc\uc5f0 \u00b7 HISTORICAL \ub77c\ubca8\uc740 \uc2e4\uc2dc\uac04 \uc2dc\uc138\uac00 \uc544\ub2d9\ub2c8\ub2e4."
        )
        summary.setObjectName("muted")
        layout.addWidget(summary)
        cards = QGridLayout()
        cards.setSpacing(SPACING_MEDIUM)
        for column, card in enumerate(
            (
                MetricCard("KOSPI", "2,650.00", "+0.84%"),
                MetricCard("S&P 500", "5,100.00", "+0.42%"),
                MetricCard("USD/KRW", "1,350.00", "-0.16%"),
            )
        ):
            cards.addWidget(card, 0, column)
        layout.addLayout(cards)
        self._chart = MarketChartPanel()
        self._chart.setObjectName("chartPanel")
        self._chart.setMinimumHeight(330)
        self._chart.symbol_changed.connect(self._refresh_chart)
        self._chart.timeframe_changed.connect(self._refresh_chart)
        self._refresh_chart()
        layout.addWidget(self._chart, 1)
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
