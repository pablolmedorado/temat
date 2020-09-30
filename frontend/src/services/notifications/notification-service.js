import { baseApiClient as SilentApi } from "../api";
import Api from "../api";
import BaseService from "../base-service";

export default class NotificationService extends BaseService {
  static baseUrlName = "common:notification";

  static unreadCount() {
    const url = Urls[`${this.baseUrlName}-unread-count`]();
    return SilentApi.get(url);
  }

  static unreadSummary() {
    return SilentApi.get(this.listUrl, { params: { unread: true, page_size: 25, page: 1 } });
  }

  static markSummaryAsRead(queryParams) {
    const url = Urls[`${this.baseUrlName}-mark-all-as-read`]();
    return SilentApi.patch(url, {}, { params: queryParams });
  }

  static markAsUnread(pk) {
    const url = Urls[`${this.baseUrlName}-mark-as-unread`]({ pk });
    return SilentApi.patch(url);
  }

  static markAsRead(pk) {
    const url = Urls[`${this.baseUrlName}-mark-as-read`]({ pk });
    return SilentApi.patch(url);
  }

  static markAllAsUnread(queryParams) {
    const url = Urls[`${this.baseUrlName}-mark-all-as-unread`]();
    return Api.patch(url, {}, { params: queryParams });
  }

  static markAllAsRead(queryParams) {
    const url = Urls[`${this.baseUrlName}-mark-all-as-read`]();
    return Api.patch(url, {}, { params: queryParams });
  }

  static bulkDelete(queryParams) {
    return Api.delete(this.listUrl, { params: queryParams });
  }
}
