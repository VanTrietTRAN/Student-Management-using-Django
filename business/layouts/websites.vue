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
                            <IconWebsite class="w-20 h-20 text-white" />
                            <h5>{{ t('Website') }}</h5>
                        </template>
                        <el-menu-item index="/websites">
                            <IconDashboard class="el-icon" />
                            <span>{{ t('Dashboard') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/websites/students">
                            <IconUsers class="el-icon" />
                            <span>{{ t('Quản lý sinh viên') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/websites/classes">
                            <IconCalendar class="el-icon" />
                            <span>{{ t('Quản lý lớp học') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/websites/subjects">
                            <Document class="el-icon" />
                            <span>{{ t('Quản lý môn học') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/websites/grades">
                            <IconAppraisal class="el-icon" />
                            <span>{{ t('Quản lý điểm số') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/websites/schedule">
                            <IconCalendar class="el-icon" />
                            <span>{{ t('Lịch học & thi') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/websites/tuition">
                            <IconFile class="el-icon" />
                            <span>{{ t('Quản lý học phí') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/websites/notifications">
                            <IconBulb class="el-icon" />
                            <span>{{ t('Thông báo') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/websites/rewards">
                            <IconAppraisal class="el-icon" />
                            <span>{{ t('Khen thưởng & Kỷ luật') }}</span>
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
import IconWebsite from "~/assets/icons/website.svg";
import IconDashboard from "~/assets/icons/dashboard.svg";
import IconUsers from "~/assets/icons/users.svg";
import IconCalendar from "~/assets/icons/calendar.svg";
import IconFile from "~/assets/icons/file.svg";
import IconAppraisal from "~/assets/icons/appraisal.svg";
import IconBulb from "~/assets/icons/bulb.svg";
import { Document } from '@element-plus/icons-vue';
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
