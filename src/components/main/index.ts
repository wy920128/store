import { ref } from "vue";
import type { Category } from "../../types/category";
import type { Software } from "../../types/software";

const cats = ref<Category[]>([]);
const list = ref<Software[]>([]);
const currentCatId = ref<number>(0);
const currentPage = ref<number>(1);
const pageSize = ref<number>(9);
const total = ref<number>(0);

export function useMain() {
  return {
    cats,
    list,
    currentCatId,
    currentPage,
    pageSize,
    total,
  };
}

export function setCategories(data: Category[]) {
  cats.value = data;
}

export function setList(data: Software[]) {
  list.value = data;
}

export function setCurrentCatId(id: number) {
  currentCatId.value = id;
}

export function setPage(p: number) {
  currentPage.value = p;
}

export function setTotal(count: number) {
  total.value = count;
}
