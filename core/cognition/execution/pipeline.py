from typing import Any, Callable, Dict, List, Optional


class PipelineStep:
    """Represents an individual step in an execution pipeline."""

    def __init__(self, name: str, action: Callable[..., Any]):
        self.name = name
        self.action = action

    def execute(self, context: Dict[str, Any]) -> Any:
        return self.action(context)


class ExecutionPipeline:
    """Sequential engine for executing modular cognitive workflows."""

    def __init__(self):
        self._steps: List[PipelineStep] = []

    def add_step(self, name: str, action: Callable[..., Any]) -> "ExecutionPipeline":
        self._steps.append(PipelineStep(name, action))
        return self

    def run(self, initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = initial_context or {}
        results = {}

        for step in self._steps:
            output = step.execute(context)
            results[step.name] = output
            context[step.name] = output

        return {"status": "success", "results": results, "final_context": context}
