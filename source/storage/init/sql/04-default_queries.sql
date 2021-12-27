\set MEMORY_CAPACITY_EXPONENT 30 -- 1GB memory limit (2^30)

INSERT INTO memory_limit (capacity) VALUES (POWER(2,:MEMORY_CAPACITY_EXPONENT));

INSERT INTO crawler_option (keyword, description) VALUES
('same_domain', 'Stay within the same domain'),
('diff_domain', 'Only visit pages from different domains');