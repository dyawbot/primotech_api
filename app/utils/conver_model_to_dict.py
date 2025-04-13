from sqlalchemy.orm import class_mapper

def model_to_dict(model):
    """Convert SQLAlchemy model to a dictionary."""
    return {column.key: getattr(model, column.key) for column in class_mapper(model.__class__).columns}