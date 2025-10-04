import BaseService from '../base';

class AcademicService extends BaseService {
  get entity() {
    return 'websites';
  }

  // Subjects
  getSubjects(params = null) {
    return this.request().get(`${this.entity}/subjects`, params);
  }

  createSubject(data) {
    return this.request().post(`${this.entity}/subjects`, data);
  }

  updateSubject(id, data) {
    return this.request().put(`${this.entity}/subjects/${id}`, data);
  }

  // Students
  getStudents(params = null) {
    return this.request().get(`${this.entity}/students`, params);
  }

  // Teachers
  getTeachers(params = null) {
    return this.request().get(`${this.entity}/teachers`, params);
  }

  getStudent(id) {
    return this.request().get(`${this.entity}/students/${id}`);
  }

  // Classrooms
  getClassrooms(params = null) {
    return this.request().get(`${this.entity}/classrooms`, params);
  }

  createStudent(data) {
    return this.request().post(`${this.entity}/students`, data);
  }

  updateStudent(id, data) {
    return this.request().put(`${this.entity}/students/${id}`, data);
  }

  // Registrations
  register(registrationData) {
    return this.request().post(`${this.entity}/registrations/register`, registrationData);
  }

  unregister(id) {
    return this.request().post(`${this.entity}/registrations/${id}/unregister`);
  }

  // Tuitions
  getTuitions(params = null) {
    return this.request().get(`${this.entity}/tuitions`, params);
  }

  payTuition(id) {
    return this.request().post(`${this.entity}/tuitions/${id}/pay`);
  }

  // Grades
  getGrades(params = null) {
    return this.request().get(`${this.entity}/grades`, params);
  }

  createGrade(data) {
    return this.request().post(`${this.entity}/grades`, data);
  }

  // Notifications
  getNotifications(params = null) {
    return this.request().get(`${this.entity}/notifications`, params);
  }

  // Schedules
  getSchedules(params = null) {
    return this.request().get(`${this.entity}/schedules`, params);
  }

  createSchedule(data) {
    return this.request().post(`${this.entity}/schedules`, data);
  }

  updateSchedule(id, data) {
    return this.request().put(`${this.entity}/schedules/${id}`, data);
  }

  deleteSchedule(id) {
    return this.request().delete(`${this.entity}/schedules/${id}`);
  }

  // Rewards / Records
  getRewards(params = null) {
    return this.request().get(`${this.entity}/rewards`, params);
  }

  createReward(data) {
    return this.request().post(`${this.entity}/rewards`, data);
  }

  updateReward(id, data) {
    return this.request().put(`${this.entity}/rewards/${id}`, data);
  }

  deleteReward(id) {
    return this.request().delete(`${this.entity}/rewards/${id}`);
  }
}

export default new AcademicService();
