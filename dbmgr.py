import sqlite3

def create_exclusion_clauses(exclusion_array):
    exclusion_array = ["\"%" + exc + "%\"" for exc in exclusion_array]
    ING_FIELD = "ingredients_english"
    initial_filter_clause = ING_FIELD + " NOT LIKE " + exclusion_array[0]    
    return initial_filter_clause + " " + " ".join(["AND " + ING_FIELD + " NOT LIKE " + exc for exc in exclusion_array[1:]])


def create_inclusion_clauses(inclusion_array):
    inclusion_array = ["\"%" + inc + "%\"" for inc in inclusion_array]
    ING_FIELD = "long_name"
    initial_filter_clause = ING_FIELD + " LIKE " + inclusion_array[0]
    return initial_filter_clause + " " + " ".join(["AND " + ING_FIELD + " LIKE " + inc for inc in inclusion_array[1:]])

def construct_search_query(excluded_ings=[], search_terms=[], limit=0):
    basis_query = "SELECT long_name, gtin_upc, manufacturer, ingredients_english FROM Products"
    full_query = basis_query
    if len(excluded_ings) > 0 or len(search_terms) > 0:
        full_query = full_query + " WHERE" 

    if len(excluded_ings) > 0:
        full_query = full_query + " " + "(" + create_exclusion_clauses(excluded_ings) + ")"

    if len(search_terms) > 0 and len(excluded_ings) > 0:
        full_query = full_query + " AND"

    if len(search_terms) > 0:
        full_query = full_query + " " + "(" + create_inclusion_clauses(search_terms) + " " + ")"

    full_query = full_query + "collate nocase"

    if limit > 0:
        full_query = full_query + " LIMIT " + str(limit)

    
    return full_query

    
