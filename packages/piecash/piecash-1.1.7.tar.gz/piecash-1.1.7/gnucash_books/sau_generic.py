import sqlalchemy as sa
from sqlalchemy import create_engine, event, and_
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker, relationship, foreign, remote, backref
from sqlalchemy_utils import generic_relationship


@as_declarative()
class Base:
    pass


engine = create_engine("sqlite://")
session = sessionmaker(bind=engine)()


class HasAddresses(object):
    """HasAddresses mixin, creates a relationship to
    the address_association table for each parent.

    """


class User(HasAddresses, Base):
    __tablename__ = "user"
    id = sa.Column(sa.Integer, primary_key=True)


class Customer(HasAddresses, Base):
    __tablename__ = "customer"
    id = sa.Column(sa.Integer, primary_key=True)


class Event(Base):
    __tablename__ = "event"
    id = sa.Column(sa.Integer, primary_key=True)

    # This is used to discriminate between the linked tables.
    object_type = sa.Column(sa.Unicode(255))

    # This is used to point to the primary key of the linked row.
    object_id = sa.Column(sa.Integer)

    @property
    def parent(self):
        """Provides in-Python access to the "parent" by choosing
        the appropriate relationship.

        """
        return getattr(self, "parent_%s" % self.object_type)

    @parent.setter
    def parent(self, value):
        value.__class__.__name__.lower()
        old_parent = self.parent
        self.object_type = value.__class__.__name__.lower()
        self.object_id = value.id
        session.expire(old_parent)


@event.listens_for(HasAddresses, "mapper_configured", propagate=True)
def setup_listener(mapper, class_):
    name = class_.__name__
    discriminator = name.lower()
    class_.object = relationship(
        Event,
        primaryjoin=and_(
            class_.id == foreign(remote(Event.object_id)),
            Event.object_type == discriminator,
        ),
        backref=backref(
            "parent_%s" % discriminator,
            primaryjoin=and_(
                remote(class_.id) == foreign(Event.object_id),
                Event.object_type == discriminator,
            ),
        ),
    )

    @event.listens_for(class_.object, "append")
    def append_address(target, value, initiator):
        value.object_type = discriminator


Base.metadata.create_all(engine)

if True:
    # Some general usage to attach an event to a user.
    user = User()
    for c in range(1):
        customer = Customer()
        session.add(customer)
    session.add_all([user])
    session.commit()

    ev = Event()
    user.object = [ev]
    ev1 = Event()
    customer.object = [ev1]
    # ev.parent = customer

    session.add(ev)
    session.commit()

if True:
    customer = session.query(Customer).all()[0]
    user = session.query(User).all()[0]
    ev = session.query(Event).all()[0]

# Find the event we just made.
print(ev.parent)

# ev.parent = customer
# print(ev.parent)
# session.commit()
# print(ev.parent)

# Find any events that are bound to users.
for ev in session.query(Event).all():
    print("-", ev, ev.parent)

for ev in session.query(Event).filter(Event.parent_user != None).all():
    print("o", ev, ev.parent)

for ev in session.query(Event).filter_by(parent_user=user).all():
    print("x", ev, ev.parent)
print(user.object)
print(customer.object)
print(ev, ev.parent)
ev.parent = customer
# session.commit()
print(user.object)
print(customer.object)
print(ev, ev.parent)
