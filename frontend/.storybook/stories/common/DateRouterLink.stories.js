// Utilities
import { storyFactory } from "../../util/helpers";
import { text } from "@storybook/addon-knobs";

// Components
import DateRouterLink from "@/components/common/DateRouterLink";

export default { title: "Components/Common/DateRouterLink" };

const story = storyFactory({ DateRouterLink });

export const Today = () =>
  story({
    props: {
      date: {
        default: text("Date", new Date().toISOString().split("T")[0]),
      },
    },
    template: `
      <DateRouterLink :date="date"></DateRouterLink>
    `,
  });
