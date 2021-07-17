import BaseService from "@/services/base-service";

class UserStoryTypeService extends BaseService {
  basename = "scrum:user-story-type";
  defaultListParams = { ordering: "name" };
}

const service = Object.freeze(new UserStoryTypeService());

export default service;
