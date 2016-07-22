create_option_types = \
    "CREATE TABLE public.option_types("\
    "id integer NOT NULL DEFAULT nextval('option_types_id_seq'::regclass),"\
    "name character varying,"\
    "created_at timestamp without time zone NOT NULL,"\
    "updated_at timestamp without time zone NOT NULL,"\
    "CONSTRAINT option_types_pkey PRIMARY KEY (id));"

create_option_value_variants = \
    "CREATE TABLE public.option_value_variants("\
    "id integer NOT NULL DEFAULT nextval('option_value_variants_id_seq'::regclass),"\
    "option_value_id integer,"\
    "variant_id integer,"\
    "created_at timestamp without time zone NOT NULL,"\
    "updated_at timestamp without time zone NOT NULL,"\
    "CONSTRAINT option_value_variants_pkey PRIMARY KEY (id));"\

create_option_values = \
    "CREATE TABLE public.option_values("\
    "id integer NOT NULL DEFAULT nextval('option_values_id_seq'::regclass),"\
    "option_type_id integer,"\
    "name character varying,"\
    "created_at timestamp without time zone NOT NULL,"\
    "updated_at timestamp without time zone NOT NULL,"\
    "CONSTRAINT option_values_pkey PRIMARY KEY (id));"

create_product_categories = \
    "CREATE TABLE public.product_categories("\
    "id integer NOT NULL DEFAULT nextval('product_categories_id_seq'::regclass),"\
    "product_id integer,"\
    "category_id integer,"\
    "created_at timestamp without time zone NOT NULL,"\
    "updated_at timestamp without time zone NOT NULL,"\
    "CONSTRAINT product_categories_pkey PRIMARY KEY (id));"

create_product_files = \
    "CREATE TABLE public.product_files("\
    "id integer NOT NULL DEFAULT nextval('product_files_id_seq'::regclass),"\
    "product_id integer,"\
    "file_type character varying,"\
    "file character varying,"\
    "cover_image character varying,"\
    "specification text,"\
    "small_version_url character varying,"\
    "normal_version_url character varying,"\
    "large_version_url character varying,"\
    "created_at timestamp without time zone NOT NULL,"\
    "updated_at timestamp without time zone NOT NULL,"\
    "CONSTRAINT product_files_pkey PRIMARY KEY (id));"

create_product_option_types = \
    "CREATE TABLE public.product_option_types("\
    "id integer NOT NULL DEFAULT nextval('product_option_types_id_seq'::regclass),"\
    "product_id integer,"\
    "option_type_id integer,"\
    "created_at timestamp without time zone NOT NULL,"\
    "updated_at timestamp without time zone NOT NULL,"\
    "CONSTRAINT product_option_types_pkey PRIMARY KEY (id));"

create_products = \
    "CREATE TABLE public.products("\
    "id integer NOT NULL DEFAULT nextval('products_id_seq'::regclass),"\
    "name character varying,"\
    "brand character varying,"\
    "product_code character varying,"\
    "created_at timestamp without time zone NOT NULL,"\
    "updated_at timestamp without time zone NOT NULL,"\
    "description text,"\
    "price_range character varying,"\
    "tsv tsvector,"\
    "category_hierarchy character varying,"\
    "shipping_info character varying,"\
    "vendor_url character varying,"\
    "product_files jsonb NOT NULL DEFAULT '[]'::jsonb,"\
    "post_id integer,"\
    "CONSTRAINT products_pkey PRIMARY KEY (id));"

create_stores = \
    "CREATE TABLE public.stores("\
    "name text,"\
    "created_at timestamp without time zone,"\
    "updated_at timestamp without time zone,"\
    "id integer NOT NULL DEFAULT nextval('stores_id_seq'::regclass));"

create_variant_files = \
    "CREATE TABLE public.variant_files("\
    "id integer NOT NULL DEFAULT nextval('variant_files_id_seq'::regclass),"\
    "variant_id integer,"\
    "file_type character varying,"\
    "file character varying,"\
    "cover_image character varying,"\
    "specification text,"\
    "small_version_url character varying,"\
    "normal_version_url character varying,"\
    "large_version_url character varying,"\
    "created_at timestamp without time zone NOT NULL,"\
    "updated_at timestamp without time zone NOT NULL,"\
    "CONSTRAINT variant_files_pkey PRIMARY KEY (id));"

create_variant_stores = \
    "CREATE TABLE public.variant_stores("\
    "id integer NOT NULL DEFAULT nextval('variant_stores_id_seq'::regclass),"\
    "price numeric(8,2),"\
    "currency character varying,"\
    "url character varying,"\
    "variant_id integer,"\
    "created_at timestamp without time zone NOT NULL,"\
    "updated_at timestamp without time zone NOT NULL,"\
    "sku character varying,"\
    "store_id integer,"\
    "quantity integer,"\
    "CONSTRAINT variant_stores_pkey PRIMARY KEY (id));"

create_variants = \
    "CREATE TABLE public.variants("\
    "id integer NOT NULL DEFAULT nextval('variants_id_seq'::regclass),"\
    "product_id integer,"\
    "created_at timestamp without time zone NOT NULL,"\
    "updated_at timestamp without time zone NOT NULL,"\
    "description character varying,"\
    "variant_files jsonb NOT NULL DEFAULT '[]'::jsonb,"\
    "\"position\" integer,"\
    "CONSTRAINT variants_pkey PRIMARY KEY (id));"