import BaseService from "../base-service";

class TagService extends BaseService {
  baseUrlName = "common:tag";
}

const service = Object.freeze(new TagService());

export default service;
