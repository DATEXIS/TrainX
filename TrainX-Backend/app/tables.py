def create_tables(db):
    # create_all() issues querys that check for the existence of
    # each indiviual table and, and if not found will issue CREATE statements
    db.create_all()
    db.session.commit()
