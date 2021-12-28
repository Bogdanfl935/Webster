CREATE FUNCTION verify_foreign_table_reference()
    RETURNS trigger AS
$BODY$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM user_record WHERE id = new.user_id) THEN
        RAISE foreign_key_violation USING MESSAGE = 'User id ' || new.user_id || ' does not exist';
    END IF;

    RETURN NEW;
END;
$BODY$
    LANGUAGE plpgsql;

DO $$
DECLARE
    iterator text;
BEGIN
    FOR iterator IN SELECT table_name FROM information_schema.columns WHERE column_name = 'user_id'
    LOOP
        EXECUTE format('CREATE TRIGGER verify_foreign_table_references
                        BEFORE INSERT ON %I FOR EACH ROW EXECUTE PROCEDURE verify_foreign_table_reference()',
                        iterator);
    END LOOP;
END;
$$ LANGUAGE plpgsql;