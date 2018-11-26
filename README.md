# toss

Toss 결제를 위한 python client library wrapper (본격 날로 먹기의 꿈)

[![CircleCI](https://circleci.com/gh/StyleShare/toss.svg?style=svg)](https://circleci.com/gh/StyleShare/toss)

## 참고자료

- [가입부터 결제 완료까지](https://tossdev.github.io/gettingstarted.html)
- [Toss Payment API](https://tossdev.github.io/api.html)

## requirements

- python3
- strong mentality

## install

> pip install toss

## usage


```python
from toss import TossPayClient

client = TossPayClient() # 아무 값도 없으면 샌드박스
```

### 결제 요청

```python
result = client.purchase(
    '주문번호', 1000, '상품설명', 'http://returning .url', False)
```

### 결제 정보 가져오기

```python
payment = client.get_payment(result.pay_token)
```

### 결제 승인 

```python
client.approve(payment.pay_token)
```

### 결제 취소

```python
client.cancel(payment.pay_token, '고객 요청으로 취소')
```

### 환불

```python
client.refund(payment.token, 1000, 0)
```

## FAQ

### 왜 이렇게 코드가 엉망인가요?

제가 죽을 죄를 지었습니다. 그러니 https://github.com/styleshare/toss/pulls 굽신굽신

### 사용하는 게 너무 불편해요.

저도요. 어머 우리 통하는 게 있나봐요. https://github.com/styleshare/toss/pulls 
그런 당신을 위해 제가 특별히 마련했습니다.

### 왜 라이선스가 Public domain 인가요?

저는 [FSF](https://www.fsf.org/)를 지지합니다. 

### toss 개발자들이 욕하지 않을까요?

제가 왜 public domain 했겠어요?

### 이거 FAQ 맞나요?

눈치가 빠른 꼬맹이는 PR이나 날리라구 https://github.com/styleshare/toss/pulls 
