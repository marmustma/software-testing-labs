package ru.mospolytech.notes

import android.app.Activity
import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.ListView
import android.widget.TextView
import android.widget.Toast
import org.json.JSONArray

/** Простое приложение «Заметки» — объект тестирования ЛР7. */
class MainActivity : Activity() {

    private val notes = ArrayList<String>()
    private lateinit var adapter: ArrayAdapter<String>
    private lateinit var input: EditText
    private lateinit var counter: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        input = findViewById(R.id.note_input)
        counter = findViewById(R.id.tv_counter)
        val list = findViewById<ListView>(R.id.list_notes)

        loadNotes()
        adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, notes)
        list.adapter = adapter

        findViewById<Button>(R.id.btn_add).setOnClickListener { addNote() }
        findViewById<Button>(R.id.btn_clear).setOnClickListener {
            notes.clear()
            onNotesChanged()
        }
        // Удаление заметки долгим нажатием
        list.setOnItemLongClickListener { _, _, position, _ ->
            notes.removeAt(position)
            onNotesChanged()
            Toast.makeText(this, R.string.deleted, Toast.LENGTH_SHORT).show()
            true
        }
        updateCounter()
    }

    private fun addNote() {
        val text = input.text.toString().trim()
        if (text.isEmpty()) {
            input.error = getString(R.string.empty_error)
            return
        }
        notes.add(text)
        input.setText("")
        onNotesChanged()
    }

    private fun onNotesChanged() {
        adapter.notifyDataSetChanged()
        saveNotes()
        updateCounter()
    }

    private fun updateCounter() {
        counter.text = getString(R.string.counter, notes.size)
    }

    // Заметки хранятся в SharedPreferences и не теряются при повороте экрана,
    // сворачивании приложения и выгрузке процесса из памяти.
    private fun saveNotes() {
        val json = JSONArray()
        notes.forEach { json.put(it) }
        getSharedPreferences(PREFS, MODE_PRIVATE).edit().putString(KEY, json.toString()).apply()
    }

    private fun loadNotes() {
        val raw = getSharedPreferences(PREFS, MODE_PRIVATE).getString(KEY, "[]") ?: "[]"
        val json = JSONArray(raw)
        notes.clear()
        for (i in 0 until json.length()) notes.add(json.getString(i))
    }

    companion object {
        private const val PREFS = "notes_prefs"
        private const val KEY = "notes"
    }
}
