import pytest

from business.models.reminder_error import ReminderError
from business.models.todo import Todo
from business.services.todo_service_impl import TodoServiceImpl
from unittest.mock import MagicMock, patch

from persistence.contracts.todo_repository import TodoRepository
from persistence.entities.todo_entity import TodoEntity


class TestRemoveTodo:
    def test_removable_todo(self):
        # Arrange
        todo_id = 9
        entity = MagicMock(spec=TodoEntity)
        model = MagicMock(spec=Todo)
        model.is_deletable = True

        mock_todo_repo = MagicMock(spec=TodoRepository)
        mock_todo_repo.select_by_id.return_value = entity

        service = TodoServiceImpl(mock_todo_repo, None)

        # Act
        with patch.object(service, 'to_todo_from_entity') as mock_to_todo_from_entity:
            mock_to_todo_from_entity.return_value = model
            actual = service.remove(todo_id)

        # Assert
        mock_to_todo_from_entity.assert_called_once_with(entity)
        mock_todo_repo.select_by_id.assert_called_once_with(todo_id)
        mock_todo_repo.delete.assert_called_once_with(todo_id)
        assert actual == model

    def test_remove_non_exist_todo(self):
        # -- Arrange --------------------------------------------------
        todo_id = 9
        mock_todo_repo = MagicMock(spec=TodoRepository)
        mock_todo_repo.select_by_id.return_value = None
        service = TodoServiceImpl(mock_todo_repo, None)

        # -- Act  -----------------------------------------------------
        with pytest.raises(ReminderError) as ex_info:
            service.remove(todo_id)

        # -- Assert ---------------------------------------------------
        # exception => ReminderError avec code 666
        assert ex_info.value.code == 666
        # invocation de mock_todo_repo.select_by_id(todo_id) => None
        mock_todo_repo.select_by_id.assert_called_once_with(todo_id)
        # pas d'invocation mock_todo_repo.delete(todo_id)
        mock_todo_repo.delete.assert_not_called()

    def test_non_removable_todo(self):
        # Arrange
        todo_id = 9
        entity = MagicMock(spec=TodoEntity)
        model = MagicMock(spec=Todo)
        model.is_deletable = False

        mock_todo_repo = MagicMock(spec=TodoRepository)
        mock_todo_repo.select_by_id.return_value = entity

        service = TodoServiceImpl(mock_todo_repo, None)

        # Act
        with patch.object(service, 'to_todo_from_entity') as mock_to_todo_from_entity:
            mock_to_todo_from_entity.return_value = model
            with pytest.raises(ReminderError) as ex_info:
                service.remove(todo_id)

        # Assert
        assert ex_info.value.code == 999
        mock_to_todo_from_entity.assert_called_once_with(entity)
        mock_todo_repo.select_by_id.assert_called_once_with(todo_id)
        mock_todo_repo.delete.assert_not_called()

















