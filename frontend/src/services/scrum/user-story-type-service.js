import BaseService from "../base-service";

export default class UserStoryTypeService extends BaseService {
  static baseUrlName = "scrum:user-story-type";
  static defaultListParams = { ordering: "name" };
}
