CREATE TABLE [dbo].[fact_dataops_pipeline_log] (
    [TraceId]             VARCHAR (8000) NULL,
    [SpanId]              VARCHAR (8000) NULL,
    [PipelineName]        VARCHAR (8000) NULL,
    [StageName]           VARCHAR (8000) NULL,
    [Component]           VARCHAR (8000) NULL,
    [ExecutionStatus]     VARCHAR (8000) NULL,
    [SourceRowCount]      BIGINT         NULL,
    [TargetRowCount]      BIGINT         NULL,
    [ExecutionDurationMs] BIGINT         NULL,
    [ErrorMessage]        VARCHAR (8000) NULL,
    [Timestamp]           DATETIME2 (6)  NULL
);


GO