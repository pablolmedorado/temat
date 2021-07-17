import BaseService from "./base-service";

class TagService extends BaseService {
  basename = "common:tag";
}

const service = Object.freeze(new TagService());

export default service;
