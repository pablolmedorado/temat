import { defaultTo } from "lodash";

import Api from "./api";

export default class BaseService {
  static get listUrl() {
    return Urls[`${this.baseUrlName}-list`]();
  }

  static detailUrl(pk) {
    return Urls[`${this.baseUrlName}-detail`]({ pk });
  }

  static list(queryParams) {
    return Api.get(this.listUrl, { params: defaultTo(queryParams, this.defaultListParams) });
  }

  static retrieve(pk, queryParams) {
    return Api.get(this.detailUrl(pk), {
      params: defaultTo(queryParams, this.defaultRetrieveParams)
    });
  }

  static save(payload, config = {}) {
    const method = payload.id ? "put" : "post";
    const url = payload.id ? this.detailUrl(payload.id) : this.listUrl;
    return Api[method](url, payload, config);
  }

  static update(payload, config = {}) {
    return Api.patch(this.detailUrl(payload.id), payload, config);
  }

  static delete(pk) {
    return Api.delete(this.detailUrl(pk));
  }
}
