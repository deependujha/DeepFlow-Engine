"""Unit tests for deepflow_engine collisions module."""

import pytest
from deepflow_engine.collisions import Event


class TestEventDataclass:
    """Test Event dataclass."""

    def test_event_creation(self):
        """Test creating an Event instance."""
        event = Event(frame=143, time=2.38, type="crash")
        assert event.frame == 143
        assert event.time == 2.38
        assert event.type == "crash"

    def test_event_fields(self):
        """Test Event has expected fields."""
        event = Event(frame=100, time=1.67, type="collision")
        assert hasattr(event, "frame")
        assert hasattr(event, "time")
        assert hasattr(event, "type")

    def test_event_is_frozen(self):
        """Test Event is immutable (frozen)."""
        event = Event(frame=50, time=0.83, type="impact")
        with pytest.raises(AttributeError):
            event.frame = 100

    def test_event_repr(self):
        """Test Event string representation."""
        event = Event(frame=10, time=0.167, type="test")
        repr_str = repr(event)
        assert "Event" in repr_str
        assert "10" in repr_str
        assert "test" in repr_str

    def test_multiple_events_with_different_types(self):
        """Test creating multiple events with different types."""
        events = [
            Event(frame=1, time=0.017, type="crash"),
            Event(frame=2, time=0.033, type="bounce"),
            Event(frame=3, time=0.050, type="collision"),
        ]
        assert len(events) == 3
        assert events[0].type == "crash"
        assert events[1].type == "bounce"
        assert events[2].type == "collision"

    @pytest.mark.parametrize(
        "frame,time,event_type",
        [
            (0, 0.0, "start"),
            (60, 1.0, "crash"),
            (3600, 60.0, "end"),
        ],
    )
    def test_event_parametrized(self, frame, time, event_type):
        """Test creating events with various parameters."""
        event = Event(frame=frame, time=time, type=event_type)
        assert event.frame == frame
        assert event.time == time
        assert event.type == event_type
