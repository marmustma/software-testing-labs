// Нагрузочный тест k6: виртуальные пользователи отправляют GET-запросы к API.
// Параметры нагрузки задаются переменными окружения:
//   k6 run -e VUS=10 -e DURATION=30s load_test.js
//   k6 run -e VUS=50 -e DURATION=10s load_test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:8000';

export const options = {
  vus: Number(__ENV.VUS || 10),
  duration: __ENV.DURATION || '30s',
  thresholds: {
    http_req_failed: ['rate<0.01'],     // ошибок меньше 1 %
    http_req_duration: ['p(95)<500'],   // 95 % запросов быстрее 500 мс
    checks: ['rate>0.99'],
  },
};

export default function () {
  const res = http.get(`${BASE_URL}/api/products?page=${1 + (__ITER % 10)}&size=10`);
  check(res, {
    'статус 200': (r) => r.status === 200,
    'в ответе 10 товаров': (r) => r.json('items').length === 10,
    'время ответа < 500 мс': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
