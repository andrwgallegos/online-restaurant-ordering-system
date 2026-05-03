"""Populate the database with sample data for demo and testing.

Run from the project root:

    python -m api.seed
"""
from datetime import date, timedelta
from decimal import Decimal

from .dependencies.database import Base, SessionLocal, engine
from .models import (
    customers,
    menu_items,
    order_items,
    orders,
    payments,
    promotions,
    recipes,
    resources,
    reviews,
)



def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)



def seed():
    db = SessionLocal()
    try:
        sample_resources = [
            resources.Resource(resource_name="Bread", stock_amount=Decimal("80"), unit="loaves"),
            resources.Resource(resource_name="Lettuce", stock_amount=Decimal("5"), unit="heads"),
            resources.Resource(resource_name="Tomato", stock_amount=Decimal("40"), unit="lbs"),
            resources.Resource(resource_name="Chicken", stock_amount=Decimal("60"), unit="lbs"),
            resources.Resource(resource_name="Cheese", stock_amount=Decimal("8"), unit="lbs"),
            resources.Resource(resource_name="Beef Patty", stock_amount=Decimal("100"), unit="patties"),
            resources.Resource(resource_name="Tofu", stock_amount=Decimal("25"), unit="blocks"),
        ]
        db.add_all(sample_resources)
        db.flush()

        sample_menu_items = [
            menu_items.MenuItem(
                name="Classic Cheeseburger",
                description="Quarter pound beef patty with cheddar, lettuce, tomato.",
                ingredients_summary="Beef patty, cheese, lettuce, tomato, bread",
                price=Decimal("9.99"),
                calories=720,
                food_category="burgers",
                is_available=True,
            ),
            menu_items.MenuItem(
                name="Grilled Chicken Sandwich",
                description="Grilled chicken breast with lettuce and tomato.",
                ingredients_summary="Chicken, lettuce, tomato, bread",
                price=Decimal("8.49"),
                calories=540,
                food_category="sandwiches",
                is_available=True,
            ),
            menu_items.MenuItem(
                name="Garden Veggie Wrap",
                description="Lettuce, tomato, and tofu wrapped in fresh bread.",
                ingredients_summary="Lettuce, tomato, tofu, bread",
                price=Decimal("7.49"),
                calories=380,
                food_category="vegetarian",
                is_available=True,
            ),
            menu_items.MenuItem(
                name="Spicy Buffalo Chicken",
                description="Crispy chicken tossed in spicy buffalo sauce.",
                ingredients_summary="Chicken, bread, buffalo sauce",
                price=Decimal("9.49"),
                calories=620,
                food_category="spicy",
                is_available=True,
            ),
            menu_items.MenuItem(
                name="Kids Cheese Sandwich",
                description="Simple cheese sandwich on soft bread.",
                ingredients_summary="Cheese, bread",
                price=Decimal("4.99"),
                calories=300,
                food_category="kids",
                is_available=True,
            ),
        ]
        db.add_all(sample_menu_items)
        db.flush()

        cheeseburger, grilled_chicken, veggie_wrap, buffalo_chicken, kids_cheese = sample_menu_items
        bread, lettuce, tomato, chicken, cheese, beef, tofu = sample_resources

        sample_recipes = [
            recipes.Recipe(menu_item_id=cheeseburger.id, resource_id=beef.id, amount_required=Decimal("1")),
            recipes.Recipe(menu_item_id=cheeseburger.id, resource_id=cheese.id, amount_required=Decimal("0.1")),
            recipes.Recipe(menu_item_id=cheeseburger.id, resource_id=bread.id, amount_required=Decimal("1")),
            recipes.Recipe(menu_item_id=grilled_chicken.id, resource_id=chicken.id, amount_required=Decimal("0.4")),
            recipes.Recipe(menu_item_id=grilled_chicken.id, resource_id=bread.id, amount_required=Decimal("1")),
            recipes.Recipe(menu_item_id=veggie_wrap.id, resource_id=tofu.id, amount_required=Decimal("0.5")),
            recipes.Recipe(menu_item_id=veggie_wrap.id, resource_id=lettuce.id, amount_required=Decimal("0.25")),
            recipes.Recipe(menu_item_id=buffalo_chicken.id, resource_id=chicken.id, amount_required=Decimal("0.4")),
            recipes.Recipe(menu_item_id=kids_cheese.id, resource_id=cheese.id, amount_required=Decimal("0.1")),
            recipes.Recipe(menu_item_id=kids_cheese.id, resource_id=bread.id, amount_required=Decimal("1")),
        ]
        db.add_all(sample_recipes)

        sample_promotions = [
            promotions.Promotion(
                code="WELCOME10",
                description="10% off for first-time customers",
                discount_type="percentage",
                discount_value=Decimal("10"),
                expiration_date=date.today() + timedelta(days=30),
                is_active=True,
            ),
            promotions.Promotion(
                code="LUNCH5",
                description="$5 off lunch orders",
                discount_type="flat",
                discount_value=Decimal("5"),
                expiration_date=date.today() + timedelta(days=14),
                is_active=True,
            ),
        ]
        db.add_all(sample_promotions)

        sample_customers = [
            customers.Customer(
                full_name="Andrew Gallegos",
                email="andrew@example.com",
                phone_number="555-123-4567",
                address="123 Main St, Charlotte, NC",
            ),
            customers.Customer(
                full_name="Dalia Foster",
                email="dalia@example.com",
                phone_number="555-987-6543",
                address="500 Oak Ave, Charlotte, NC",
            ),
        ]
        db.add_all(sample_customers)
        db.flush()

        andrew, dalia = sample_customers

        first_order = orders.Order(
            customer_id=andrew.id,
            tracking_number="ORD-DEMO0001",
            order_status="completed",
            fulfillment_type="delivery",
            subtotal=Decimal("18.48"),
            discount_amount=Decimal("0.00"),
            total_price=Decimal("18.48"),
            delivery_address="123 Main St, Charlotte, NC",
            special_instructions="Ring doorbell twice",
        )
        second_order = orders.Order(
            customer_id=dalia.id,
            tracking_number="ORD-DEMO0002",
            order_status="preparing",
            fulfillment_type="takeout",
            subtotal=Decimal("12.48"),
            discount_amount=Decimal("1.25"),
            total_price=Decimal("11.23"),
            delivery_address="500 Oak Ave, Charlotte, NC",
            special_instructions=None,
        )
        db.add_all([first_order, second_order])
        db.flush()

        sample_order_items = [
            order_items.OrderItem(
                order_id=first_order.id,
                menu_item_id=cheeseburger.id,
                quantity=1,
                unit_price=Decimal("9.99"),
                line_total=Decimal("9.99"),
            ),
            order_items.OrderItem(
                order_id=first_order.id,
                menu_item_id=grilled_chicken.id,
                quantity=1,
                unit_price=Decimal("8.49"),
                line_total=Decimal("8.49"),
            ),
            order_items.OrderItem(
                order_id=second_order.id,
                menu_item_id=veggie_wrap.id,
                quantity=1,
                unit_price=Decimal("7.49"),
                line_total=Decimal("7.49"),
            ),
            order_items.OrderItem(
                order_id=second_order.id,
                menu_item_id=kids_cheese.id,
                quantity=1,
                unit_price=Decimal("4.99"),
                line_total=Decimal("4.99"),
            ),
        ]
        db.add_all(sample_order_items)

        sample_payments = [
            payments.Payment(
                order_id=first_order.id,
                payment_type="credit_card",
                transaction_status="completed",
                amount=Decimal("18.48"),
                card_last4="1234",
                payment_reference="PAY-DEMO0001",
            ),
            payments.Payment(
                order_id=second_order.id,
                payment_type="debit_card",
                transaction_status="completed",
                amount=Decimal("11.23"),
                card_last4="5678",
                payment_reference="PAY-DEMO0002",
            ),
        ]
        db.add_all(sample_payments)

        sample_reviews = [
            reviews.Review(
                customer_id=andrew.id,
                order_id=first_order.id,
                menu_item_id=cheeseburger.id,
                rating=5,
                review_text="Best cheeseburger in Charlotte!",
            ),
            reviews.Review(
                customer_id=dalia.id,
                order_id=second_order.id,
                menu_item_id=veggie_wrap.id,
                rating=4,
                review_text="Fresh and tasty, would order again.",
            ),
            reviews.Review(
                customer_id=andrew.id,
                order_id=first_order.id,
                menu_item_id=grilled_chicken.id,
                rating=2,
                review_text="Chicken was a bit dry today.",
            ),
        ]
        db.add_all(sample_reviews)

        db.commit()
        print("Sample data loaded successfully.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()



if __name__ == "__main__":
    reset_database()
    seed()
