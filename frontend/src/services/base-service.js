import { defaultTo } from "lodash";

import Api from "@/utils/api";

export default class BaseService {
  get listUrl() {
    return Urls[`${this.basename}-list`]();
  }

  detailUrl(pk) {
    return Urls[`${this.basename}-detail`]({ pk });
  }

  list(queryParams) {
    return Api.get(this.listUrl, { params: defaultTo(queryParams, this.defaultListParams) });
  }

  retrieve(pk, queryParams) {
    return Api.get(this.detailUrl(pk), {
      params: defaultTo(queryParams, this.defaultRetrieveParams),
    });
  }

  save(payload, queryParams) {
    const method = payload.id ? "put" : "post";
    const url = payload.id ? this.detailUrl(payload.id) : this.listUrl;
    return Api[method](url, payload, { params: queryParams });
  }

  update(payload, queryParams) {
    return Api.patch(this.detailUrl(payload.id), payload, { params: queryParams });
  }

  delete(pk) {
    return Api.delete(this.detailUrl(pk));
  }
}
