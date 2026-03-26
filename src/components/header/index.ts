import { ref } from "vue";
import type { SystemInfo } from "../../types/system";

const sysInfo = ref<SystemInfo>({
  name: "",
  major: 1,
  minor: 0,
  patch: 0,
  author: "",
});

const keyword = ref<string>("");

export function useHeader() {
  return {
    sysInfo,
    keyword,
  };
}

export function setSysInfo(data: SystemInfo) {
  Object.assign(sysInfo.value, data);
}
