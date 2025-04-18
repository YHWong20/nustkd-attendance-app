class Member:
    """
    Member class
    """

    def __init__(self, name, status):
        self.name = name
        self.status = status
        self.member_id = f"{status.lower()}-{name.replace(' ', '').lower()}"

    def __repr__(self):
        return f"Student({self.name}, {self.status}) - {self.member_id}"

    def __eq__(self, other):
        if isinstance(other, Member):
            return (self.status == other.status) and (self.member_id == other.member_id)
        return False

    def __hash__(self):
        return hash(self.member_id)
