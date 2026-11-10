CREATE TABLE IF NOT EXISTS pipeline_batches (
    batch_id UUID PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ,
    status VARCHAR(20) NOT NULL CHECK (status IN ('RUNNING', 'SUCCESS', 'FAILED')),
    records_extracted INTEGER NOT NULL DEFAULT 0 CHECK (records_extracted >= 0),
    records_loaded INTEGER NOT NULL DEFAULT 0 CHECK (records_loaded >= 0),
    records_quarantined INTEGER NOT NULL DEFAULT 0 CHECK (records_quarantined >= 0),
    error_message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_events (
    id BIGSERIAL PRIMARY KEY,
    batch_id UUID NOT NULL REFERENCES pipeline_batches(batch_id),
    source VARCHAR(100) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    interval VARCHAR(10) NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clean_events (
    symbol VARCHAR(20) NOT NULL,
    interval VARCHAR(10) NOT NULL,
    open_time TIMESTAMPTZ NOT NULL,
    close_time TIMESTAMPTZ NOT NULL,
    open NUMERIC(30, 15) NOT NULL CHECK (open > 0),
    high NUMERIC(30, 15) NOT NULL CHECK (high > 0),
    low NUMERIC(30, 15) NOT NULL CHECK (low > 0),
    close NUMERIC(30, 15) NOT NULL CHECK (close > 0),
    volume NUMERIC(30, 15) NOT NULL CHECK (volume >= 0),
    source VARCHAR(50) NOT NULL,
    batch_id UUID NOT NULL REFERENCES pipeline_batches(batch_id),
    ingested_at TIMESTAMPTZ NOT NULL,
    CONSTRAINT pk_clean_events PRIMARY KEY (symbol, interval, open_time),
    CONSTRAINT ck_clean_events_price_range CHECK (
        high >= low AND high >= open AND high >= close
        AND low <= open AND low <= close
    ),
    CONSTRAINT ck_clean_events_time_range CHECK (close_time > open_time)
);

CREATE INDEX IF NOT EXISTS idx_raw_events_batch_id ON raw_events(batch_id);
CREATE INDEX IF NOT EXISTS idx_raw_events_symbol ON raw_events(symbol);
CREATE INDEX IF NOT EXISTS idx_clean_events_open_time ON clean_events(open_time);
CREATE INDEX IF NOT EXISTS idx_clean_events_symbol_interval
    ON clean_events(symbol, interval);
CREATE INDEX IF NOT EXISTS idx_pipeline_batches_started_at
    ON pipeline_batches(started_at DESC);
