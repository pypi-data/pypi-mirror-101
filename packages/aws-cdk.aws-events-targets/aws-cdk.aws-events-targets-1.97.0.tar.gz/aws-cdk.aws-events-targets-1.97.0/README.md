# Event Targets for Amazon EventBridge

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This library contains integration classes to send Amazon EventBridge to any
number of supported AWS Services. Instances of these classes should be passed
to the `rule.addTarget()` method.

Currently supported are:

* [Start a CodeBuild build](#start-a-codebuild-build)
* [Start a CodePipeline pipeline](#start-a-codepipeline-pipeline)
* Run an ECS task
* [Invoke a Lambda function](#invoke-a-lambda-function)
* Publish a message to an SNS topic
* Send a message to an SQS queue
* [Start a StepFunctions state machine](#start-a-stepfunctions-state-machine)
* Queue a Batch job
* Make an AWS API call
* Put a record to a Kinesis stream
* [Log an event into a LogGroup](#log-an-event-into-a-loggroup)
* Put a record to a Kinesis Data Firehose stream
* Put an event on an EventBridge bus

See the README of the `@aws-cdk/aws-events` library for more information on
EventBridge.

## Event retry policy and using dead-letter queues

The Codebuild, CodePipeline, Lambda, StepFunctions and LogGroup targets support attaching a [dead letter queue and setting retry policies](https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html). See the [lambda example](#invoke-a-lambda-function).
Use [escape hatches](https://docs.aws.amazon.com/cdk/latest/guide/cfn_layer.html) for the other target types.

## Invoke a Lambda function

Use the `LambdaFunction` target to invoke a lambda function.

The code snippet below creates an event rule with a Lambda function as a target
triggered for every events from `aws.ec2` source. You can optionally attach a
[dead letter queue](https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html).

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_events as events
import aws_cdk.aws_sqs as sqs
import aws_cdk.aws_events_targets as targets
import aws_cdk.core as cdk


fn = lambda_.Function(self, "MyFunc",
    runtime=lambda_.Runtime.NODEJS_12_X,
    handler="index.handler",
    code=lambda_.Code.from_inline(f"exports.handler = {handler.toString()}")
)

rule = events.Rule(self, "rule",
    event_pattern=EventPattern(
        source=["aws.ec2"]
    )
)

queue = sqs.Queue(self, "Queue")

rule.add_target(targets.LambdaFunction(fn,
    dead_letter_queue=queue, # Optional: add a dead letter queue
    max_event_age=cdk.Duration.hours(2), # Otional: set the maxEventAge retry policy
    retry_attempts=2
))
```

## Log an event into a LogGroup

Use the `LogGroup` target to log your events in a CloudWatch LogGroup.

For example, the following code snippet creates an event rule with a CloudWatch LogGroup as a target.
Every events sent from the `aws.ec2` source will be sent to the CloudWatch LogGroup.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_logs as logs
import aws_cdk.aws_events as events
import aws_cdk.aws_events_targets as targets


log_group = logs.LogGroup(self, "MyLogGroup",
    log_group_name="MyLogGroup"
)

rule = events.Rule(self, "rule",
    event_pattern=EventPattern(
        source=["aws.ec2"]
    )
)

rule.add_target(targets.CloudWatchLogGroup(log_group))
```

## Start a CodeBuild build

Use the `CodeBuildProject` target to trigger a CodeBuild project.

The code snippet below creates a CodeCommit repository that triggers a CodeBuild project
on commit to the master branch. You can optionally attach a
[dead letter queue](https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html).

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_sdk.aws_codebuild as codebuild
import aws_sdk.aws_codecommit as codecommit
import aws_sdk.aws_sqs as sqs
import aws_cdk.aws_events_targets as targets


repo = codecommit.Repository(self, "MyRepo",
    repository_name="aws-cdk-codebuild-events"
)

project = codebuild.Project(self, "MyProject",
    source=codebuild.Source.code_commit(repository=repo)
)

dead_letter_queue = sqs.Queue(self, "DeadLetterQueue")

# trigger a build when a commit is pushed to the repo
on_commit_rule = repo.on_commit("OnCommit",
    target=targets.CodeBuildProject(project,
        dead_letter_queue=dead_letter_queue
    ),
    branches=["master"]
)
```

## Start a CodePipeline pipeline

Use the `CodePipeline` target to trigger a CodePipeline pipeline.

The code snippet below creates a CodePipeline pipeline that is triggered every hour

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_sdk.aws_codepipeline as codepipeline
import aws_sdk.aws_sqs as sqs


pipeline = codepipeline.Pipeline(self, "Pipeline")

rule = events.Rule(stack, "Rule",
    schedule=events.Schedule.expression("rate(1 hour)")
)

rule.add_target(targets.CodePipeline(pipeline))
```

## Start a StepFunctions state machine

Use the `SfnStateMachine` target to trigger a State Machine.

The code snippet below creates a Simple StateMachine that is triggered every minute with a
dummy object as input.
You can optionally attach a
[dead letter queue](https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html)
to the target.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_sdk.aws_iam as iam
import aws_sdk.aws_sqs as sqs
import aws_cdk.aws_stepfunctions as sfn
import aws_cdk.aws_events_targets as targets


rule = events.Rule(stack, "Rule",
    schedule=events.Schedule.rate(cdk.Duration.minutes(1))
)

dlq = sqs.Queue(stack, "DeadLetterQueue")

role = iam.Role(stack, "Role",
    assumed_by=iam.ServicePrincipal("events.amazonaws.com")
)
state_machine = sfn.StateMachine(stack, "SM",
    definition=sfn.Wait(stack, "Hello", time=sfn.WaitTime.duration(cdk.Duration.seconds(10))),
    role=role
)

rule.add_target(targets.SfnStateMachine(state_machine,
    input=events.RuleTargetInput.from_object(SomeParam="SomeValue"),
    dead_letter_queue=dlq
))
```
