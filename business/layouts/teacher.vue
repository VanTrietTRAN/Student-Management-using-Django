<template>
    <div class="w-full h-full flex bg-tertiary-light align-center justify-center">
        <div v-if="!authenticated" class="lg:py-20 py-6">
            <LoginForm>
                <div class="flex text-center justify-center">
                    <AmozLogo class="h-20" />
                </div>
                <div class="my-5">
                    <p class="lg:text-l text-center font-bold">
                        {{ $t("welcome_to_amoz") }}
                    </p>
                </div>
            </LoginForm>
        </div>
        <div v-else class="absolute w-full">
            <TopbarNav />
            <div class="flex flex-row">
                <aside>
                    <Sidebar>
                        <template #header>
                            <IconUsers class="w-20 h-20 text-white" />
                            <h5>{{ t('Giảng viên') }}</h5>
                        </template>
                        <el-menu-item index="/websites/teacher-dashboard">
                            <IconDashboard class="el-icon" />
                            <span>{{ t('Dashboard') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/websites/teacher-schedule">
                            <IconCalendar class="el-icon" />
                            <span>{{ t('Lịch dạy') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/websites/teacher-classes">
                            <IconUsers class="el-icon" />
                            <span>{{ t('Lớp học') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/websites/teacher-grades">
                            <IconAppraisal class="el-icon" />
                            <span>{{ t('Nhập điểm') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/websites/teacher-notifications">
                            <IconBulb class="el-icon" />
                            <span>{{ t('Thông báo') }}</span>
                        </el-menu-item>
                    </Sidebar>
                </aside>
                <div class="flex-auto">
                    <slot />
                </div>
            </div>
            <footer class="w-full bg-gray-100 flex justify-center">
                <FooterContent />
            </footer>
        </div>
    </div>
</template>

<script setup>
import AmozLogo from "/assets/icons/Logo.svg";
import IconUsers from "~/assets/icons/users.svg";
import IconDashboard from "~/assets/icons/dashboard.svg";
import IconCalendar from "~/assets/icons/calendar.svg";
import IconAppraisal from "~/assets/icons/appraisal.svg";
import IconBulb from "~/assets/icons/bulb.svg";
import { useOauthStore } from "@/stores/oauth";

const { t } = useI18n();

const oauthStore = useOauthStore();
const authenticated = computed(() => {
    const { tokenInfo } = oauthStore;
    if (!tokenInfo) return false;
    const { access_token } = tokenInfo;
    if (!access_token) return false;
    return access_token.length > 0;
});
</script>

<style scoped></style>
