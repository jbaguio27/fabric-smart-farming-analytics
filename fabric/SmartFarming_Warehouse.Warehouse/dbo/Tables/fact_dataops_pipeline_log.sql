CREATE TABLE [dbo].[fact_dataops_pipeline_log] (
    [Component]           VARCHAR (8000) NULL,
    [ErrorMessage]        VARCHAR (8000) NULL,
    [ExecutionDurationMs] BIGINT         NULL,
    [ExecutionStatus]     VARCHAR (8000) NULL,
    [PipelineName]        VARCHAR (8000) NULL,
    [SourceRowCount]      BIGINT         NULL,
    [SpanId]              VARCHAR (8000) NULL,
    [StageName]           VARCHAR (8000) NULL,
    [TargetRowCount]      BIGINT         NULL,
    [Timestamp]           DATETIME2 (6)  NULL,
    [TraceId]             VARCHAR (8000) NULL
);


GO