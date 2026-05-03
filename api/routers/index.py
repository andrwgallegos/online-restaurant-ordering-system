from . import (
    checkout,
    customers,
    menu_items,
    order_items,
    orders,
    payments,
    promotions,
    recipes,
    reports,
    resources,
    reviews,
)



def load_routes(app):
    app.include_router(customers.router)
    app.include_router(menu_items.router)
    app.include_router(resources.router)
    app.include_router(recipes.router)
    app.include_router(promotions.router)
    app.include_router(orders.router)
    app.include_router(order_items.router)
    app.include_router(payments.router)
    app.include_router(reviews.router)
    app.include_router(checkout.router)
    app.include_router(reports.router)
