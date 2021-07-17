// Utilities
import { storyFactory } from "../../util/helpers";
import { object } from "@storybook/addon-knobs";

// Components
import GroupPill from "@/components/GroupPill";

export default { title: "Components/Common/GroupPill" };

const story = storyFactory({ GroupPill });

export const Default = () => {
  return story({
    props: {
      group: {
        default: object("Group", {
          name: "Test Group",
        }),
      },
    },
    template: `
      <GroupPill :group="group"></GroupPill>
    `,
  });
};
