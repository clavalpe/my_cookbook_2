from unittest.mock import MagicMock, create_autospec

import pytest
from sqlalchemy.orm import Session

from my_cookbook.recipes.infrastructure.dependencies import get_session


class TestGetSession:
    @pytest.fixture
    def mock_session(self) -> MagicMock:
        session: MagicMock = create_autospec(Session, spec_set=True, instance=True)
        return session

    def test_keeps_the_work_of_a_request_that_succeeds(
        self, mock_session: MagicMock
    ) -> None:
        sessions = get_session(MagicMock(return_value=mock_session))

        assert next(sessions) is mock_session
        with pytest.raises(StopIteration):
            next(sessions)

        mock_session.commit.assert_called_once_with()
        mock_session.rollback.assert_not_called()
        mock_session.close.assert_called_once_with()

    def test_abandons_the_work_of_a_request_that_fails(
        self, mock_session: MagicMock
    ) -> None:
        sessions = get_session(MagicMock(return_value=mock_session))
        next(sessions)

        with pytest.raises(RuntimeError):
            sessions.throw(RuntimeError())

        mock_session.rollback.assert_called_once_with()
        mock_session.commit.assert_not_called()
        mock_session.close.assert_called_once_with()
