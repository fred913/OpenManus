"""Collection classes for managing multiple tools."""

from typing import Any, Type, TypeVar, cast

from app.exceptions import ToolError
from app.tool.base import BaseTool, ToolFailure, ToolResult


T = TypeVar("T", bound=BaseTool)


class ToolCollection:
    """A collection of defined tools."""

    def __init__(self, *tools: BaseTool):
        self.tools = tools
        self.tool_map = {tool.name: tool for tool in tools}

    def __iter__(self):
        return iter(self.tools)

    def to_params(self) -> list[dict[str, Any]]:
        return [tool.to_param() for tool in self.tools]

    async def execute(
        self, *, name: str, tool_input: dict[str, Any] | None = None
    ) -> ToolResult:
        tool = self.tool_map.get(name)
        if not tool:
            return ToolFailure(error=f"Tool {name} is invalid")
        try:
            result = await tool(**(tool_input or {}))
            return result
        except ToolError as e:
            return ToolFailure(error=e.message)

    async def execute_all(self) -> list[ToolResult]:
        """Execute all tools in the collection sequentially."""
        results = []
        for tool in self.tools:
            try:
                result = await tool()
                results.append(result)
            except ToolError as e:
                results.append(ToolFailure(error=e.message))
        return results

    def get_tool(self, tool_type: Type[T]) -> T:
        name: str = cast(Any, tool_type)().name
        res = self.tool_map.get(name)
        assert res is not None, f"Tool {name} is not defined"
        assert isinstance(
            res, tool_type
        ), f"Tool {name} is not an instance of {tool_type.__name__}"
        return res

    def add_tool(self, tool: BaseTool):
        self.tools += (tool,)
        self.tool_map[tool.name] = tool
        return self

    def add_tools(self, *tools: BaseTool):
        for tool in tools:
            self.add_tool(tool)
        return self
