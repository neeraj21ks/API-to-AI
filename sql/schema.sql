 CREATE TABLE IF NOT EXISTS raw_events(
    id BIGSERIAL PRIMARY KEY,
    
    batch_id VARCHAR(100) NOT NULL,
    source VARCHAR(100) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    interval VARCHAR(10) NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
 );

 CREATE TABLE IF NOT EXISTS clean_events(
    symbol VARCHAR(20) NOT NULL,
    interval VARCHAR(10) NOT NULL,

    open_time TIMESTAMPTZ NOT NULL,
    close_time TIMESTAMPTZ NOT NULL,

    open NUMERIC(30, 15) NOT NULL,
    high NUMERIC(30, 15) NOT NULL,
    low NUMERIC(30, 15) NOT NULL,
    close NUMERIC(30, 15) NOT NULL,
    volume NUMERIC(30, 15) NOT NULL,

    source VARCHAR(50) NOT NULL,
    batch_id VARCHAR(100) NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT pk_clean_events
        PRIMARY KEY (symbol, interval, open_time)
);

CREATE INDEX IF NOT EXISTS idx_raw_events_batch_id
    ON raw_events(batch_id);

CREATE INDEX IF NOT EXISTS idx_raw_events_symbol
    ON raw_events(symbol);

CREATE INDEX IF NOT EXISTS idx_clean_events_open_time
    ON clean_events(open_time);

CREATE INDEX IF NOT EXISTS idx_clean_events_symbol_interval
    ON clean_events(symbol, interval);