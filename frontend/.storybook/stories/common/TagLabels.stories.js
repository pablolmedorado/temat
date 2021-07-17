// Utilities
import { storyFactory } from "../../util/helpers";
import { object } from "@storybook/addon-knobs";

// Components
import TagLabels from "@/components/TagLabels";

export default { title: "Components/Common/TagLabels" };

const story = storyFactory({ TagLabels });

export const Default = () => {
  return story({
    props: {
      tags: {
        default: object("Tags", ["Tag 1", "Tag 2", "Tag with length > 20 characters"]),
      },
    },
    template: `
      <TagLabels :tags="tags"></TagLabels>
    `,
  });
};
