"""Implementations for Sprite class.
"""

from typing import Optional

from apysc.display.child_interface import ChildInterface
from apysc.display.display_object import DisplayObject
from apysc.display.graphics import Graphics
from apysc.display.stage import Stage
from apysc.type import Array
from apysc.type.revert_interface import RevertInterface


class Sprite(DisplayObject, ChildInterface, RevertInterface):

    graphics: Graphics

    def __init__(
            self, stage: Stage,
            variable_name: Optional[str] = None) -> None:
        """
        Basic display object that can be parent.

        Parameters
        ----------
        stage : Stage
            Stage instance to link this object.
        variable_name : str or None, default None
            Variable name of this instance. This will be used to
            js expression. It is not necessary to specify any
            string except when Sprite subclass will be instantiated.
        """
        from apysc.expression import expression_variables_util
        from apysc.expression import var_names

        # Graphics sprite child cound of 1.
        self._js_child_adjust_num = 1

        if variable_name is None:
            variable_name = expression_variables_util.\
                get_next_variable_name(type_name=var_names.SPRITE)
        self._children = Array([])
        super(Sprite, self).__init__(
            stage=stage, variable_name=variable_name)
        self._append_constructor_expression()
        self.graphics = Graphics(parent=self)

    def _append_constructor_expression(self) -> bool:
        """
        Append Sprite constructor expression.

        Notes
        -----
        Expression not to be added if instance is Sprite subclass.

        Returns
        -------
        appended : bool
            If expression appended, then True will be set.
        """
        from apysc.display.stage import get_stage_variable_name
        from apysc.expression import expression_file_util
        from apysc.type import type_util
        is_same_class_instance: bool = type_util.is_same_class_instance(
            class_=Sprite, instance=self)
        if not is_same_class_instance:
            return False
        stage_variable_name: str = get_stage_variable_name()
        expression: str = (
            f'\nvar {self.variable_name} = {stage_variable_name}.group();'
        )
        expression_file_util.append_js_expression(expression=expression)
        return True

    def _make_snapshot(self, snapshot_name: str) -> None:
        """
        Make values snapshot.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
        if self._snapshot_exists(snapshot_name=snapshot_name):
            return
        self.graphics._run_all_make_snapshot_methods(
            snapshot_name=snapshot_name)

    def _revert(self, snapshot_name: str) -> None:
        """
        Revert values if snapshot exists.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
        if not self._snapshot_exists(snapshot_name=snapshot_name):
            return
        self.graphics._run_all_revert_methods(snapshot_name=snapshot_name)
