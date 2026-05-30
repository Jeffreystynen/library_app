"""Prediction Service - Reading completion predictions using linear regression."""
from datetime import datetime, timedelta
import math


class PredictionService:
    """Service for predicting book reading completion times using regression."""

    @staticmethod
    def fit_linear_regression(daily_data):
        """Fit ordinary least squares linear regression to daily reading data.

        Args:
            daily_data: list of dicts with 'session_date' (date or datetime) and 'pages_read' (int)

        Returns:
            dict with keys:
                - slope: pages/day (float)
                - intercept: baseline pages (float)
                - r_squared: goodness of fit (float, 0-1)
                - predicted_pages_per_day: fitted slope at x=session_count (float)
                - sessions_used: number of sessions (int)

            If fewer than 3 data points, returns fallback with slope=0 (simple average),
            r_squared=0 (undefined fit)
        """
        if not daily_data:
            return {
                "slope": 0,
                "intercept": 0,
                "r_squared": 0,
                "predicted_pages_per_day": 0,
                "sessions_used": 0,
            }

        n = len(daily_data)

        if n < 3:
            # Fallback: simple average pages/day
            total_pages = sum(d["pages_read"] for d in daily_data)
            avg_pages = total_pages / n if n > 0 else 0
            return {
                "slope": 0,
                "intercept": 0,
                "r_squared": 0,
                "predicted_pages_per_day": avg_pages,
                "sessions_used": n,
            }

        # Compute OLS: x = day index (0, 1, 2, ..., n-1), y = pages_read
        x_values = list(range(n))
        y_values = [d["pages_read"] for d in daily_data]

        x_mean = sum(x_values) / n
        y_mean = sum(y_values) / n

        # Covariance and variance
        numerator = sum((x_values[i] - x_mean) * (y_values[i] - y_mean) for i in range(n))
        denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            # All x values same (only one unique date or all x values constant)
            avg_pages = y_mean
            return {
                "slope": 0,
                "intercept": avg_pages,
                "r_squared": 0,
                "predicted_pages_per_day": avg_pages,
                "sessions_used": n,
            }

        slope = numerator / denominator
        intercept = y_mean - slope * x_mean

        # R-squared: 1 - (SS_res / SS_tot)
        ss_tot = sum((y - y_mean) ** 2 for y in y_values)
        ss_res = sum((y_values[i] - (slope * x_values[i] + intercept)) ** 2 for i in range(n))

        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        r_squared = max(0, min(1, r_squared))  # Clamp to [0, 1]

        # Predicted pages/day: use the average (more realistic than trend slope)
        # The slope represents trend over time, not actual reading rate
        predicted_pages_per_day = y_mean if y_mean > 0.1 else max(0.1, slope)

        return {
            "slope": slope,
            "intercept": intercept,
            "r_squared": r_squared,
            "predicted_pages_per_day": predicted_pages_per_day,
            "sessions_used": n,
        }

    @staticmethod
    def predict_completion(book, model):
        """Predict completion date for a book.

        Args:
            book: dict with keys 'id', 'title', 'pages'
            model: dict from fit_linear_regression (slope, intercept, r_squared, etc.)

        Returns:
            dict with keys:
                - book_id: (int)
                - title: (str)
                - pages_remaining: (int)
                - predicted_pages_per_day: (float)
                - days_remaining: (float)
                - estimated_finish_date: (str, ISO format)
                - model: (dict with slope, intercept, r_squared, sessions_used)
        """
        book_id = book.get("id")
        title = book.get("title")
        total_pages = book.get("pages", 0)
        pages_read = book.get("pages_read", 0)

        pages_remaining = max(0, total_pages - pages_read)
        predicted_pages_per_day = model.get("predicted_pages_per_day", 1)

        if predicted_pages_per_day <= 0:
            predicted_pages_per_day = 1

        days_remaining = pages_remaining / predicted_pages_per_day if predicted_pages_per_day > 0 else 0

        today = datetime.now().date()
        estimated_finish_date = (today + timedelta(days=days_remaining)).isoformat()

        return {
            "book_id": book_id,
            "title": title,
            "pages_remaining": pages_remaining,
            "predicted_pages_per_day": round(predicted_pages_per_day, 2),
            "days_remaining": round(days_remaining, 1),
            "estimated_finish_date": estimated_finish_date,
            "model": {
                "sessions_used": model.get("sessions_used", 0),
                "slope": round(model.get("slope", 0), 2),
                "intercept": round(model.get("intercept", 0), 2),
                "r_squared": round(model.get("r_squared", 0), 2),
            },
        }
