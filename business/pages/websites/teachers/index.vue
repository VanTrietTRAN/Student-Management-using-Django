<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Quản lý giảng viên</h1>
                    <p class="text-gray-600">Quản lý thông tin giảng viên, phân công giảng dạy</p>
                </div>
                <el-button type="primary" :icon="Plus" @click="showAddDialog = true">
                    Thêm giảng viên mới
                </el-button>
            </div>
        </div>

        <!-- Search and Filter Section -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <el-input
                    v-model="searchKeyword"
                    placeholder="Tìm kiếm theo tên giảng viên..."
                    :prefix-icon="Search"
                    clearable
                />
                <el-select v-model="selectedDepartment" placeholder="Chọn khoa" clearable>
                    <el-option label="Tất cả khoa" value="" />
                    <el-option label="Khoa CNTT" value="CNTT" />
                    <el-option label="Khoa KTPM" value="KTPM" />
                    <el-option label="Khoa ATTT" value="ATTT" />
                </el-select>
                <el-select v-model="selectedStatus" placeholder="Chọn trạng thái" clearable>
                    <el-option label="Tất cả trạng thái" value="" />
                    <el-option label="Đang làm việc" value="Đang làm việc" />
                    <el-option label="Nghỉ hưu" value="Nghỉ hưu" />
                    <el-option label="Tạm nghỉ" value="Tạm nghỉ" />
                </el-select>
                <el-button type="primary" :icon="Search" @click="handleSearch">
                    Tìm kiếm
                </el-button>
            </div>
        </div>

        <!-- Statistics Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6">
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
                <div class="flex items-center">
                    <div class="p-3 bg-blue-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-blue-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng giảng viên</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalTeachers }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Đang làm việc</p>
                        <p class="text-2xl font-bold text-gray-900">{{ activeTeachers }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
                <div class="flex items-center">
                    <div class="p-3 bg-purple-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-purple-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Khoa CNTT</p>
                        <p class="text-2xl font-bold text-gray-900">{{ cnttTeachers }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconCalendar class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng môn dạy</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalSubjects }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Teachers Table -->
        <div class="bg-white rounded-lg shadow-md">
            <div class="p-6 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Danh sách giảng viên</h3>
            </div>
            <div class="overflow-x-auto">
                <el-table :data="filteredTeachers" stripe style="width: 100%">
                    <el-table-column prop="teacherId" label="Mã GV" width="120" />
                    <el-table-column prop="fullName" label="Họ và tên" width="200" />
                    <el-table-column prop="email" label="Email" width="200" />
                    <el-table-column prop="phone" label="Số điện thoại" width="130" />
                    <el-table-column prop="department" label="Khoa" width="120" />
                    <el-table-column prop="status" label="Trạng thái" width="120">
                        <template #default="scope">
                            <el-tag :type="getStatusType(scope.row.status)">
                                {{ scope.row.status }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="Thao tác" width="200">
                        <template #default="scope">
                            <el-button size="small" @click="viewTeacher(scope.row)">
                                Xem
                            </el-button>
                            <el-button size="small" type="primary" @click="editTeacher(scope.row)">
                                Sửa
                            </el-button>
                            <el-button size="small" type="danger" @click="deleteTeacher(scope.row)">
                                Xóa
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div class="p-4 border-t border-gray-200">
                <el-pagination
                    v-model:current-page="currentPage"
                    v-model:page-size="pageSize"
                    :page-sizes="[10, 20, 50, 100]"
                    :total="totalTeachers"
                    layout="total, sizes, prev, pager, next, jumper"
                />
            </div>
        </div>

        <!-- Add Teacher Dialog -->
        <el-dialog v-model="showAddDialog" title="Thêm giảng viên mới" width="600px">
            <el-form :model="newTeacher" label-width="120px">
                <el-form-item label="Mã giảng viên">
                    <el-input v-model="newTeacher.teacherId" />
                </el-form-item>
                <el-form-item label="Họ và tên">
                    <el-input v-model="newTeacher.fullName" />
                </el-form-item>
                <el-form-item label="Email">
                    <el-input v-model="newTeacher.email" type="email" />
                </el-form-item>
                <el-form-item label="Số điện thoại">
                    <el-input v-model="newTeacher.phone" />
                </el-form-item>
                <el-form-item label="Khoa">
                    <el-select v-model="newTeacher.department" placeholder="Chọn khoa">
                        <el-option label="Khoa CNTT" value="CNTT" />
                        <el-option label="Khoa KTPM" value="KTPM" />
                        <el-option label="Khoa ATTT" value="ATTT" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Ảnh thẻ">
                    <input type="file" accept="image/*" @change="onAddImageChange" />
                    <div v-if="newTeacher.profile_picture_preview" class="mt-2">
                        <img :src="newTeacher.profile_picture_preview" alt="Preview" class="w-24 h-24 object-cover rounded-full border" />
                    </div>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showAddDialog = false">Hủy</el-button>
                <el-button type="primary" @click="addTeacher">Thêm</el-button>
            </template>
        </el-dialog>

        <!-- View Teacher Dialog -->
        <el-dialog v-model="showViewDialog" title="Thông tin giảng viên" width="800px">
            <div v-if="selectedTeacher" class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                    <div class="col-span-2 flex flex-col items-center">
                        <label class="block text-sm font-medium text-gray-700">Ảnh thẻ</label>
                        <img v-if="selectedTeacher.profile_picture" :src="getProfilePictureUrl(selectedTeacher.profile_picture)" alt="Ảnh thẻ" class="w-32 h-32 object-cover rounded-full border mb-2" />
                        <span v-else class="text-gray-400">Chưa có ảnh</span>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Mã giảng viên</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedTeacher.teacherId }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Họ và tên</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedTeacher.fullName }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Email</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedTeacher.email }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Số điện thoại</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedTeacher.phone }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Khoa</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedTeacher.department }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Trạng thái</label>
                        <el-tag :type="getStatusType(selectedTeacher.status)">
                            {{ selectedTeacher.status }}
                        </el-tag>
                    </div>
                </div>
            </div>
            <template #footer>
                <el-button @click="showViewDialog = false">Đóng</el-button>
                <el-button type="primary" @click="editTeacherFromView">Chỉnh sửa</el-button>
            </template>
        </el-dialog>

        <!-- Edit Teacher Dialog -->
        <el-dialog v-model="showEditDialog" title="Chỉnh sửa giảng viên" width="600px">
            <el-form :model="editingTeacher" label-width="120px">
                <el-form-item label="Mã giảng viên">
                    <el-input v-model="editingTeacher.teacherId" disabled />
                </el-form-item>
                <el-form-item label="Họ và tên">
                    <el-input v-model="editingTeacher.fullName" />
                </el-form-item>
                <el-form-item label="Email">
                    <el-input v-model="editingTeacher.email" type="email" />
                </el-form-item>
                <el-form-item label="Số điện thoại">
                    <el-input v-model="editingTeacher.phone" />
                </el-form-item>
                <el-form-item label="Khoa">
                    <el-select v-model="editingTeacher.department" placeholder="Chọn khoa">
                        <el-option label="Khoa CNTT" value="CNTT" />
                        <el-option label="Khoa KTPM" value="KTPM" />
                        <el-option label="Khoa ATTT" value="ATTT" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Trạng thái">
                    <el-select v-model="editingTeacher.status" placeholder="Chọn trạng thái">
                        <el-option label="Đang làm việc" value="Đang làm việc" />
                        <el-option label="Nghỉ hưu" value="Nghỉ hưu" />
                        <el-option label="Tạm nghỉ" value="Tạm nghỉ" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Ảnh thẻ">
                    <input type="file" accept="image/*" @change="onEditImageChange" />
                    <div v-if="editingTeacher.profile_picture_preview || editingTeacher.profile_picture" class="mt-2">
                        <img :src="editingTeacher.profile_picture_preview || getProfilePictureUrl(editingTeacher.profile_picture)" alt="Preview" class="w-24 h-24 object-cover rounded-full border" />
                    </div>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showEditDialog = false">Hủy</el-button>
                <el-button type="primary" @click="updateTeacher">Cập nhật</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, Search } from '@element-plus/icons-vue';
import IconUsers from '@/assets/icons/users.svg';
import IconAppraisal from '@/assets/icons/appraisal.svg';
import IconCalendar from '@/assets/icons/calendar.svg';
import { onMounted } from 'vue'
import AcademicService from '@/services/websites/academic'

definePageMeta({ layout: 'websites' });

import type { Teacher, NewTeacher, EditingTeacher } from '@/types/websites/teacher';

// Reactive data
const searchKeyword = ref('');
const selectedDepartment = ref('');
const selectedStatus = ref('');
const currentPage = ref(1);
const pageSize = ref(20);
const showAddDialog = ref(false);
const showViewDialog = ref(false);
const showEditDialog = ref(false);
const selectedTeacher = ref<Teacher | null>(null);
const editingTeacher = ref<EditingTeacher>({} as EditingTeacher);

const newTeacher = ref<NewTeacher>({
    teacherId: '',
    fullName: '',
    email: '',
    phone: '',
    department: '',
    profile_picture: null,
    profile_picture_preview: null
});

<<<<<<< HEAD
// Teachers list (will be loaded from API)
const teachers = ref<any[]>([])

// fallback mock in case API isn't available
const fallbackTeachers = [
    { id: 1, teacherId: 'GV001', fullName: 'ThS. Nguyễn Văn A', email: 'a.nguyen@university.edu', phone: '0123456789', department: 'CNTT', status: 'Đang làm việc' },
    { id: 2, teacherId: 'GV002', fullName: 'TS. Trần Thị B', email: 'b.tran@university.edu', phone: '0987654321', department: 'CNTT', status: 'Đang làm việc' }
]

onMounted(async () => {
    try {
        const res = await AcademicService.getTeachers({ page_size: 100 })
        const data = res && res.data ? res.data : res
        teachers.value = Array.isArray(data) ? data : (data.results || [])
        if (!teachers.value.length) teachers.value = fallbackTeachers
    } catch (err) {
        console.warn('Failed to load teachers', err)
        teachers.value = fallbackTeachers
=======
// Mock data
const teachers = ref<Teacher[]>([
    {
        id: 1,
        teacherId: 'GV001',
        fullName: 'ThS. Nguyễn Văn A',
        email: 'a.nguyen@university.edu',
        phone: '0123456789',
        department: 'CNTT',
        status: 'Đang làm việc'
    },
    {
        id: 2,
        teacherId: 'GV002',
        fullName: 'TS. Trần Thị B',
        email: 'b.tran@university.edu',
        phone: '0987654321',
        department: 'CNTT',
        status: 'Đang làm việc'
    },
    {
        id: 3,
        teacherId: 'GV003',
        fullName: 'ThS. Lê Văn C',
        email: 'c.le@university.edu',
        phone: '0369852147',
        department: 'KTPM',
        status: 'Đang làm việc'
    },
    {
        id: 4,
        teacherId: 'GV004',
        fullName: 'TS. Phạm Thị D',
        email: 'd.pham@university.edu',
        phone: '0741235698',
        department: 'ATTT',
        status: 'Đang làm việc'
>>>>>>> 3b3381a6d34ff10ab244e9176bf5c5305c89c0c0
    }
})

// Subjects count (for statistics card)
const subjects = ref<any[]>([])
const fallbackSubjectsCount = 15
onMounted(async () => {
    try {
        const res = await AcademicService.getSubjects({ page_size: 1 })
        const data = res && res.data ? res.data : res
        // if paginated, data.count may exist
        if (data && typeof data.count === 'number') {
            subjects.value = new Array(data.count).fill(null)
        } else {
            subjects.value = Array.isArray(data) ? data : (data.results || [])
        }
    } catch (err) {
        console.warn('Failed to load subjects count', err)
        subjects.value = []
    }

})

// Computed properties
const totalTeachers = computed(() => teachers.value.length);
const activeTeachers = computed(() => teachers.value.filter(t => t.status === 'Đang làm việc').length);
const cnttTeachers = computed(() => teachers.value.filter(t => t.department === 'CNTT').length);
const totalSubjects = computed(() => subjects.value.length || fallbackSubjectsCount)

const filteredTeachers = computed(() => {
    let filtered = teachers.value;
    
    if (searchKeyword.value) {
        filtered = filtered.filter(teacher => 
            teacher.fullName.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
            teacher.teacherId.toLowerCase().includes(searchKeyword.value.toLowerCase())
        );
    }
    
    if (selectedDepartment.value) {
        filtered = filtered.filter(teacher => teacher.department === selectedDepartment.value);
    }
    
    if (selectedStatus.value) {
        filtered = filtered.filter(teacher => teacher.status === selectedStatus.value);
    }
    
    return filtered;
});

// Methods
const getStatusType = (status: string) => {
    switch (status) {
        case 'Đang làm việc': return 'success';
        case 'Nghỉ hưu': return 'info';
        case 'Tạm nghỉ': return 'warning';
        default: return 'danger';
    }
};

const handleSearch = () => {
    ElMessage.success('Tìm kiếm hoàn tất');
};

const viewTeacher = (teacher: Teacher) => {
    selectedTeacher.value = teacher;
    showViewDialog.value = true;
};

const editTeacher = (teacher: Teacher) => {
    editingTeacher.value = {
        ...teacher,
        profile_picture: null,
        profile_picture_preview: null
    };
    showEditDialog.value = true;
};

const editTeacherFromView = () => {
    if (selectedTeacher.value) {
        showViewDialog.value = false;
        editingTeacher.value = {
            ...selectedTeacher.value,
            profile_picture: null,
            profile_picture_preview: null
        };
        showEditDialog.value = true;
    }
};


const deleteTeacher = (teacher: Teacher) => {
    ElMessageBox.confirm(
        `Bạn có chắc chắn muốn xóa giảng viên "${teacher.fullName}"?`,
        'Xác nhận xóa',
        {
            confirmButtonText: 'Xóa',
            cancelButtonText: 'Hủy',
            type: 'warning',
        }
    ).then(async () => {
        try {
            const res = await fetch(`/api/v1/websites/teachers/${teacher.id}/`, {
                method: 'DELETE',
                headers: {
                    'Accept': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                }
            });
            if (!res.ok) throw new Error('Lỗi khi xóa giảng viên');
            const index = teachers.value.findIndex(t => t.id === teacher.id);
            if (index > -1) {
                teachers.value.splice(index, 1);
                ElMessage.success(`Đã xóa giảng viên: ${teacher.fullName}`);
            }
        } catch (err) {
            ElMessage.error('Lỗi khi xóa giảng viên');
        }
    }).catch(() => {
        ElMessage.info('Đã hủy xóa giảng viên');
    });
};

// Helper to get full image URL from backend
const getProfilePictureUrl = (path: string | File | null | undefined) => {
    if (!path) return '';
    if (path instanceof File) return URL.createObjectURL(path);
    if (typeof path !== 'string') return '';
    if (path.startsWith('http')) return path;
    // Use relative path
    return `/media/${path}`;
};

// Handle image file change for add
const onAddImageChange = (e: Event) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (file) {
        newTeacher.value.profile_picture = file;
        const reader = new FileReader();
        reader.onload = (ev) => {
            newTeacher.value.profile_picture_preview = ev.target?.result as string;
        };
        reader.readAsDataURL(file);
    }
};

// Handle image file change for edit
const onEditImageChange = (e: Event) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (file) {
        editingTeacher.value.profile_picture = file;
        const reader = new FileReader();
        reader.onload = (ev) => {
            editingTeacher.value.profile_picture_preview = ev.target?.result as string;
        };
        reader.readAsDataURL(file);
    }
};

// Add teacher with image upload
const addTeacher = async () => {
    if (newTeacher.value.teacherId && newTeacher.value.fullName) {
        const formData = new FormData();
        for (const key in newTeacher.value) {
            if (key === 'profile_picture' && newTeacher.value.profile_picture instanceof File) {
                formData.append('profile_picture', newTeacher.value.profile_picture);
            } else if (key !== 'profile_picture_preview') {
                formData.append(key, String(newTeacher.value[key as keyof NewTeacher]));
            }
        }
        try {
            const res = await fetch('/api/v1/websites/teachers/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                },
                body: formData
            });
            if (!res.ok) throw new Error('Lỗi khi thêm giảng viên');
            const data = await res.json();
            teachers.value.push(data);
            showAddDialog.value = false;
            newTeacher.value = {
                teacherId: '',
                fullName: '',
                email: '',
                phone: '',
                department: '',
                profile_picture: null,
                profile_picture_preview: null
            };
            ElMessage.success('Thêm giảng viên thành công');
        } catch (err) {
            ElMessage.error('Lỗi khi thêm giảng viên');
        }
    } else {
        ElMessage.error('Vui lòng điền đầy đủ thông tin');
    }
};

<<<<<<< HEAD
// Computed properties

=======
// Update teacher with image upload
const updateTeacher = async () => {
    const index = teachers.value.findIndex(t => t.id === editingTeacher.value.id);
    if (index > -1) {
        const formData = new FormData();
        for (const key in editingTeacher.value) {
            if (key === 'profile_picture' && editingTeacher.value.profile_picture instanceof File) {
                formData.append('profile_picture', editingTeacher.value.profile_picture);
            } else if (key !== 'profile_picture_preview') {
                formData.append(key, String(editingTeacher.value[key as keyof EditingTeacher]));
            }
        }
        try {
            const res = await fetch(`/api/v1/websites/teachers/${editingTeacher.value.id}/`, {
                method: 'PUT',
                headers: {
                    'Accept': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                },
                body: formData
            });
            if (!res.ok) throw new Error('Lỗi khi cập nhật giảng viên');
            const data = await res.json();
            teachers.value[index] = data;
            showEditDialog.value = false;
            ElMessage.success(`Cập nhật giảng viên: ${editingTeacher.value.fullName}`);
        } catch (err) {
            ElMessage.error('Lỗi khi cập nhật giảng viên');
        }
    }
};
>>>>>>> 3b3381a6d34ff10ab244e9176bf5c5305c89c0c0
</script>

<style scoped>
.el-table {
    font-size: 14px;
}
</style>
