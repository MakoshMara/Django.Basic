window.onload = function () {
    let i;
    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    const quantity_arr = [];
    const price_arr = [];

    const TOTAL_FORMS = parseInt($('input[name="orderitem-TOTAL_FORMS"]').val());
    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;

    for (i = 0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name="orderitem-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitem-' + (i + 1) + '-price').text().replace(',', '.'));
        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
    }
    console.log(quantity_arr)
    console.log(price_arr)

    if (!order_total_quantity) {
        orderSummaryRecalc();
    }

    function orderSummaryRecalc() {
        order_total_quantity = 0;
        order_total_cost = 0;
        for (var i = 0; i < TOTAL_FORMS; i++) {
            order_total_quantity += quantity_arr[i];
            order_total_cost += quantity_arr[i] * price_arr[i];
        }
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(Number(order_total_cost.toFixed(2)).toString());
    }

    // {
    //     for (i = 0; i < TOTAL_FORMS; i++) {
    //         order_total_quantity += quantity_arr[i];
    //         order_total_cost += quantity_arr[i] * price_arr[i];
    //     }
    //     $('.order_total_quantity').html(order_total_quantity.toString());
    //     $('.order_total_cost').html(Number(order_total_cost.toFixed(2)).toString());
    // }

    $('.order_form').on('click', 'input[type="number"]', function () {
        var target = event.target;
        console.log(event.target)
        orderitem_num = parseInt(target.name.replace('orderitem-', '').replace('-quantity', ''));
        console.log(orderitem_num)
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
        }
    });

    $('.order_form select').change(function () {
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitem-', '').replace('-product', ''));
        var orderitem_product_pk = target.options[target.selectedIndex].value;
        if (orderitem_product_pk) {
            $.ajax({
                url: "/orders/product/" + orderitem_product_pk + "/price/",
                success: function (data) {
                    console.log(data)
                    if (data.price) {
                        price_arr[orderitem_num] = parseFloat(data.price);
                        if (isNaN(quantity_arr[orderitem_num])) {
                            quantity_arr[orderitem_num] = 0;
                        }
                        var price_html = '<span>' + data.price.toString().replace('.', ',') + '</span> руб';
                        var current_tr = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');
                        current_tr.find('td:eq(2)').html(price_html);

                        if (isNaN(current_tr.find('input[type="number"]').val())) {
                            current_tr.find('input[type="number"]').val(0);
                        }
                        orderSummaryRecalc();
                    }
                },
            });
        }
    });

    function deleteOrderItem(row) {
        var target_name = row[0].querySelector('input[type="number"]').name;
        orderitem_num = parseInt(target_name.replace('orderitem-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    }


    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity;

        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;

        $('.order_total_cost').html(order_total_cost.toString());
        $('.order_total_quantity').html(order_total_quantity.toString());
    }

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitem',
        removed: deleteOrderItem
    });
}