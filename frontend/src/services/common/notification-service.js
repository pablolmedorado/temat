import Api from "../api";
import BaseService from "../base-service";

class NotificationService extends BaseService {
  baseUrlName = "common:notification";

  unreadCount() {
    const url = Urls[`${this.baseUrlName}-unread-count`]();
    return Api.get(url);
  }

  unreadSummary() {
    return Api.get(this.listUrl, { params: { unread: true, page_size: 25, page: 1 } });
  }

  markSummaryAsRead(queryParams) {
    const url = Urls[`${this.baseUrlName}-mark-all-as-read`]();
    return Api.patch(url, {}, { params: queryParams });
  }

  markAsUnread(pk) {
    const url = Urls[`${this.baseUrlName}-mark-as-unread`]({ pk });
    return Api.patch(url);
  }

  markAsRead(pk) {
    const url = Urls[`${this.baseUrlName}-mark-as-read`]({ pk });
    return Api.patch(url);
  }

  markAllAsUnread(queryParams) {
    const url = Urls[`${this.baseUrlName}-mark-all-as-unread`]();
    return Api.patch(url, {}, { params: queryParams });
  }

  markAllAsRead(queryParams) {
    const url = Urls[`${this.baseUrlName}-mark-all-as-read`]();
    return Api.patch(url, {}, { params: queryParams });
  }

  bulkDelete(queryParams) {
    return Api.delete(this.listUrl, { params: queryParams });
  }
}

const service = Object.freeze(new NotificationService());

export default service;
