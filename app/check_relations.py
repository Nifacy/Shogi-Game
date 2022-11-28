from tortoise import Model, fields, Tortoise, run_async


class MyModel(Model):
    key = fields.IntField(default=0)

    def __str__(self):
        return f"MyModel(key={self.key})"


async def main():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()

    m = await MyModel.create()
    m.key = 10

    last_m = await MyModel.get(id=m.id)

    print(m, last_m)

    await Tortoise.close_connections()


run_async(main())
