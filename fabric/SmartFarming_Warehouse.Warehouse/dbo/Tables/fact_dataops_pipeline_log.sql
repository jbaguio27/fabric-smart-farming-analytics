CREATE TABLE [dbo].[fact_dataops_pipeline_log] (
    [TraceId]             VARCHAR (100)  NULL,
    [SpanId]              VARCHAR (50)   NULL,
    [PipelineName]        VARCHAR (100)  NULL,
    [StageName]           VARCHAR (100)  NULL,
    [Component]           VARCHAR (100)  NULL,
    [ExecutionStatus]     VARCHAR (50)   NULL,
    [SourceRowCount]      BIGINT         NULL,
    [TargetRowCount]      BIGINT         NULL,
    [ExecutionDurationMs] INT            NULL,
    [ErrorMessage]        VARCHAR (1000) NULL,
    [Timestamp]           DATETIME2 (6)  NULL
);


GO