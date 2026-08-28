import pytest
from core.cognition.execution.pipeline import ExecutionPipeline


@pytest.fixture
def pipeline():
    return ExecutionPipeline()


def test_sequential_pipeline_execution(pipeline):
    def step_one(ctx):
        return ctx.get("input", 0) + 10

    def step_two(ctx):
        return ctx.get("step_one", 0) * 2

    pipeline.add_step("step_one", step_one)
    pipeline.add_step("step_two", step_two)

    output = pipeline.run({"input": 5})

    assert output["status"] == "success"
    assert output["results"]["step_one"] == 15
    assert output["results"]["step_two"] == 30
    assert output["final_context"]["step_two"] == 30


def test_empty_pipeline_run(pipeline):
    output = pipeline.run()
    assert output["status"] == "success"
    assert output["results"] == {}
