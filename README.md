API calls for history service:

/filter                                                                        ----> getting all filters
/filter/<int:filter_id>                                                        ----> getting filter by id
/history                                                                       ----> getting all history and creating new record
/history/user/<int:user_id>                                                    ----> getting user history
/history/file/<int:file_id>                                                    ----> deleting history by file
/history/user/<int:user_id>/file/<int:file_id>/filter/<int:filter_id>          ----> getting one history record