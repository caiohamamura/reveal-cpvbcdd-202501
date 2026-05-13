For many small teams, startups, and full-stack developers, the practical appeal of MongoDB-style document databases is not primarily horizontal scaling. It is that they let you start building from the application side with less upfront database design.

A typical motivation is:

“I have an object in my code. I want to save it. Later I want to retrieve something very similar to that object.”

That fits document databases very naturally.

For example, in JavaScript/TypeScript:

const user = {
  name: "Ana",
  email: "ana@example.com",
  preferences: {
    theme: "dark",
    notifications: true
  }
}

await db.collection("users").insertOne(user)

You do not need to first define:

CREATE TABLE users (...);
CREATE TABLE user_preferences (...);
ALTER TABLE ...

So yes, MongoDB often feels code-first or application-first, while relational databases often feel more schema-first or data-model-first.

The tradeoff is that MongoDB does not remove schema design; it moves schema responsibility into the application.

In SQL, the database strongly enforces structure:

users
- id
- name
- email

user_preferences
- user_id
- theme
- notifications

In MongoDB, you may start with:

{
  name: "Ana",
  email: "ana@example.com"
}

Then later some documents have:

{
  fullName: "Ana Silva",
  emailAddress: "ana@example.com",
  preferences: {
    theme: "dark"
  }
}

Now the application has to deal with old and new shapes. That flexibility is helpful early, but it can become technical debt.

So I would phrase it like this:

Many developers choose NoSQL document databases not because they need massive horizontal scaling, but because they want fast iteration, flexible data shapes, and a development model that maps naturally to objects in code. The “no schema” benefit is really “schema later” or “schema in the application,” not truly “no schema.”

This is especially attractive when:

the product is still changing quickly;
the data model is not yet stable;
the team wants to prototype fast;
the backend mostly stores and retrieves JSON-like objects;
joins and complex relational constraints are not central.

But relational databases are often better when:

relationships between entities matter a lot;
consistency constraints are important;
reporting and analytics queries are complex;
the data model is part of the business logic;
long-term maintainability matters more than early flexibility.

In practice, a lot of the “MongoDB vs SQL” debate is less about scalability and more about where you want the structure to live:

SQL:
  structure is defined and enforced mostly by the database

MongoDB/document DB:
  structure is defined and enforced mostly by the application

That is why MongoDB feels easier at the beginning, while PostgreSQL often feels safer and clearer as the system matures.
