def create_sequence(seq_name):
    SQL =   "CREATE SEQUENCE public.{}_id_seq\n" \
            "INCREMENT 1\n" \
            "MINVALUE 1\n" \
            "MAXVALUE 9223372036854775807\n" \
            "START 1\n" \
            "CACHE 1;\n" \
            "ALTER TABLE public.{}_id_seq\n" \
            "OWNER TO postgres;\n".format(seq_name, seq_name)
    print SQL
    return  SQL
