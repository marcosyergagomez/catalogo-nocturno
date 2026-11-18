create table productos (
  code text primary key,
  product_name text not null,
  brands text,
  last_modified_t bigint not null,
  nutriscore_grade text
);