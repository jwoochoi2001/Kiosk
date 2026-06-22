from __future__ import annotations

TRANSLATIONS: dict[str, dict[str, str]] = {
    # welcome
    "welcome_subtitle": {"ko": "맛있는 커피를 주문해 보세요", "en": "Order your favorite coffee"},
    "start_order": {"ko": "주문 시작하기", "en": "Start Order"},
    "lang_switch_to_en": {"ko": "English", "en": "English"},
    "lang_switch_to_ko": {"ko": "한국어", "en": "한국어"},
    # menu
    "home": {"ko": "← 처음으로", "en": "← Home"},
    "menu_select": {"ko": "메뉴 선택", "en": "Menu"},
    "cart": {"ko": "장바구니", "en": "Cart"},
    "cart_count": {"ko": "장바구니 {count}개", "en": "{count} item(s)"},
    "cart_empty": {"ko": "담은 메뉴가 없습니다", "en": "Your cart is empty"},
    "total": {"ko": "합계  {amount}원", "en": "Total  ₩{amount}"},
    "clear_cart": {"ko": "초기화", "en": "Clear"},
    "pay": {"ko": "결제하기", "en": "Checkout"},
    "select_options": {"ko": "옵션 선택", "en": "Options"},
    "add": {"ko": "담기", "en": "Add"},
    "price_from": {"ko": "{price:,}원~", "en": "₩{price:,}~"},
    "price_line": {"ko": "{price:,}원 × {qty}", "en": "₩{price:,} × {qty}"},
    "alert_empty_cart": {"ko": "메뉴를 먼저 선택해 주세요.", "en": "Please add items to your cart first."},
    "clear_cart_title": {"ko": "장바구니 초기화", "en": "Clear Cart"},
    "clear_cart_msg": {"ko": "장바구니를 비울까요?", "en": "Clear all items from your cart?"},
    "idle_warning": {
        "ko": "선택하지 않으면 {seconds}초 후 처음 화면으로 돌아갑니다",
        "en": "Returning home in {seconds}s if no selection is made",
    },
    # categories
    "category_coffee": {"ko": "커피", "en": "Coffee"},
    "category_non_coffee": {"ko": "논커피", "en": "Non-Coffee"},
    "category_juice": {"ko": "주스", "en": "Juice"},
    "category_tea": {"ko": "티/차", "en": "Tea"},
    "category_dessert": {"ko": "디저트", "en": "Dessert"},
    # order confirm
    "back_to_menu": {"ko": "← 메뉴로", "en": "← Back to Menu"},
    "order_type_check": {"ko": "주문 방식 확인", "en": "Order Type"},
    "order_type_title": {"ko": "주문 방식을 다시 확인해 주세요", "en": "Please confirm your order type"},
    "order_type_subtitle": {
        "ko": "매장 이용과 포장 중 하나를 선택해 주세요",
        "en": "Choose dine-in or takeout",
    },
    "order_dine_in": {"ko": "매장에서 먹고 가기", "en": "Dine In"},
    "order_dine_in_desc": {"ko": "매장 내 식사", "en": "Eat in store"},
    "order_takeout": {"ko": "포장해 가기", "en": "Takeout"},
    "order_takeout_desc": {"ko": "테이크아웃 / 포장", "en": "To go / Takeaway"},
    "order_confirm_dialog_title": {"ko": "주문 방식 확인", "en": "Confirm Order Type"},
    "order_confirm_dialog_msg": {
        "ko": "「{choice}」를 선택하셨습니다.\n맞으실까요?",
        "en": 'You selected "{choice}".\nIs that correct?',
    },
    # payment
    "back": {"ko": "← 뒤로", "en": "← Back"},
    "payment": {"ko": "결제", "en": "Payment"},
    "order_summary": {"ko": "주문 내역", "en": "Order Summary"},
    "payment_method": {"ko": "결제 수단", "en": "Payment Method"},
    "pay_card": {"ko": "💳  카드", "en": "💳  Card"},
    "pay_cash": {"ko": "💵  현금", "en": "💵  Cash"},
    "pay_mobile": {"ko": "📱  모바일 결제", "en": "📱  Mobile Pay"},
    "order_type_line": {"ko": "주문 방식: {type}", "en": "Order type: {type}"},
    "total_payment": {"ko": "총 결제 금액", "en": "Total Due"},
    "payment_amount": {"ko": "결제 금액: {amount}원", "en": "Amount: ₩{amount}"},
    "won": {"ko": "{amount}원", "en": "₩{amount}"},
    "payment_confirm_title": {"ko": "결제 확인", "en": "Confirm Payment"},
    "payment_confirm_msg": {
        "ko": "{order_type}\n{method}로 {amount}원을 결제할까요?",
        "en": "{order_type}\nPay ₩{amount} with {method}?",
    },
    "method_card": {"ko": "카드", "en": "Card"},
    "method_cash": {"ko": "현금", "en": "Cash"},
    "method_mobile": {"ko": "모바일 결제", "en": "Mobile Pay"},
    "paid_with": {"ko": "{method} 결제", "en": "Paid via {method}"},
    # processing
    "payment_processing": {"ko": "결제 중입니다", "en": "Processing Payment"},
    "payment_processing_sub": {"ko": "잠시만 기다려 주세요", "en": "Please wait a moment"},
    # receipt
    "receipt_ask": {"ko": "영수증을 받으시겠습니까?", "en": "Would you like a receipt?"},
    "receipt_no": {"ko": "괜찮아요", "en": "No Thanks"},
    "receipt_yes": {"ko": "받기", "en": "Print Receipt"},
    "receipt_printed": {"ko": "영수증 출력", "en": "Receipt printed"},
    # complete
    "payment_done": {"ko": "결제가 완료되었습니다", "en": "Payment Complete"},
    "order_number": {"ko": "주문번호  {number}", "en": "Order #{number}"},
    "auto_home": {"ko": "{seconds}초 후 처음 화면으로 이동합니다", "en": "Returning home in {seconds}s"},
    "go_home": {"ko": "처음으로", "en": "Home"},
    # option dialog
    "cancel": {"ko": "취소", "en": "Cancel"},
    "extra_price": {"ko": " (+{price:,}원)", "en": " (+₩{price:,})"},
}


def translate(language: str, key: str, **kwargs) -> str:
    entry = TRANSLATIONS.get(key, {})
    text = entry.get(language, entry.get("ko", key))
    return text.format(**kwargs) if kwargs else text


def category_key(category_id: str) -> str:
    return f"category_{category_id}"
