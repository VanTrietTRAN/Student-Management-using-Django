<template>
    <div class="lg:py-10 py-6 lg:px-12 px-6 min-w-280 sm:w-full h-full bg-white rounded-lg drop-shadow-md">
        <main class="w-full">
            <div class="w-full md:max-w-[550px] max-w-[360px] mx-auto">
                <slot />
                <span v-if="store.isFirstLogin" class="mb-6">{{ $t('congrate_finishing_account') }}</span>
                <p v-if="error" class="flex self-center justify-center text-red-800 mb-2">{{ error }}</p>
                <el-form ref="formRef" :model="formData" :rules="rules"
                    class="flex flex-col justify-center items-center self-center gap-2">
                    <el-form-item prop="email">
                        <el-input v-model="formData.email" style="width: 240px" :placeholder="$t('Email')" />
                    </el-form-item>
                    <el-form-item prop="password">
                        <el-input v-model="formData.password" style="width: 240px" type="password"
                            :placeholder="t('password_place_holder')" show-password />
                    </el-form-item>
                </el-form>
                <div class="mt-6 flex flex-col justify-center items-center">
                    <el-button type="primary" @click="login()">
                        {{ $t('Login') }}
                    </el-button>
                    <NuxtLink to="/forgot-password" class="mt-6 text-primary underline">
                        {{ $t('forgot_password') }}
                    </NuxtLink>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup lang="ts">
import OAuthService from '@/services/oauth';
import { useOauthStore } from '~/stores/oauth';
import { getErrorMessage } from '@/utils/error';
import type { FormInstance, FormRules } from 'element-plus';

interface LoginForm {
    email: string | null;
    password: string | null;
}

interface LoginResponse {
    access_token: string;
    refresh_token: string;
    redirect_to?: string;
}

interface User {
    id: string;
    email: string;
    [key: string]: any;
}

const props = defineProps<{
    redirectTo?: string;
}>();

const { t } = useI18n();
const store = useOauthStore();

const formRef = ref<FormInstance>();
const formData = ref<LoginForm>({
    email: null,
    password: null
});
const error = ref<string | null>(null);

const login = async () => {
    if (!formRef.value) {
        return;
    }

    try {
        await formRef.value.validate();
        
        const { email, password } = formData.value;
        if (!email || !password) {
            return;
        }

        store.setFirstLogin(false);
        error.value = null;

        try {
            const response = await OAuthService.login({ username: email, password }) as LoginResponse;
            const { access_token, refresh_token } = response;
            
            if (access_token && refresh_token) {
                store.setTokenInfo({ access_token, refresh_token });
                try {
                    const user = await OAuthService.userinfo() as User;
                    store.setUser(user);
                    
                    if (props.redirectTo) {
                        navigateTo(props.redirectTo);
                    }
                } catch (e) {
                    error.value = getErrorMessage(e, t('an_error_occurred'));
                }
            }
        } catch (e) {
            error.value = getErrorMessage(e, t('an_error_occurred'));
        }
    } catch {
        // Form validation failed
        return;
    }
};

const rules = reactive<FormRules>({
    email: [
        { required: true, message: t('validate_error_required'), trigger: 'blur' },
        { type: 'email', message: t('validate_error_email_format'), trigger: ['blur'] },
    ],
    password: [
        { required: true, message: t('validate_error_required'), trigger: 'blur' },
    ],
});
</script>

<style scoped>
a {
    text-decoration: none;
}
</style>