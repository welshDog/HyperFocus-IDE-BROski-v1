import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

export let errorRate = new Rate('errors');

export let options = {
  stages: [
    { duration: '5m', target: 200 }, // ramp up to 200 users over 5 minutes
    { duration: '10m', target: 200 }, // stay at 200 users for 10 minutes
    { duration: '5m', target: 0 },   // ramp down to 0 users
  ],
  thresholds: {
    'http_req_duration': ['p(95)<300'], // 95% of requests must complete below 300ms
    'errors': ['rate<0.001'], // error rate should be less than 0.1%
  },
};

export default function () {
  let url = __ENV.TARGET_URL || 'http://hypercode-core:8000/health';
  let res = http.get(url);
  let result = check(res, {
    'status is 200': (r) => r.status === 200,
  });
  if (!result) {
    errorRate.add(1);
  }
  sleep(1);
}
