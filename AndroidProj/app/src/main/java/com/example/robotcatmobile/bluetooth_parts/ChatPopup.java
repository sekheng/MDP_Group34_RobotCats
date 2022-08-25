package com.example.robotcatmobile.bluetooth_parts;

import android.annotation.SuppressLint;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.inputmethod.EditorInfo;
import android.widget.Button;
import android.widget.EditText;
import android.widget.PopupWindow;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.robotcatmobile.R;

import java.nio.charset.Charset;
import java.util.ArrayList;

// for just the chat!
public class ChatPopup extends PopupWindow {
    // to get the broadcast
    public static final String CHAT_BROADCAST = "incomingMessage";
    // to get the value by using this key to access the broadcast's extra
    public static final String RECEIVE_MESSAGE = "receivedMessage";

    public RecyclerView mChatRecycler;

    public EditText mUserInput;

    public Button mSendButton;

    BroadcastReceiver mChatBR = new BroadcastReceiver() {
        @SuppressLint("MissingPermission")
        @Override
        public void onReceive(Context context, Intent intent) {
            addTxtToChat(BluetoothConn.instance.mDevice.getName() + ": " + intent.getStringExtra(RECEIVE_MESSAGE));
        }
    };

    public ChatPopup(View contentView, int width, int height)
    {
        super(contentView, width, height, true);
        // then we will have to handle the recycler!
        mChatRecycler = contentView.findViewById(R.id.bluetooth_chat_view);
        ChatViewRecycler chatViewRecycler = new ChatViewRecycler();
        mChatRecycler.setAdapter(chatViewRecycler);
        mChatRecycler.setLayoutManager(new LinearLayoutManager(contentView.getContext(), LinearLayoutManager.VERTICAL, false));
        // get the remaining UI
        mUserInput = contentView.findViewById(R.id.input_text);
        mUserInput.setOnEditorActionListener((textView, i, keyEvent) -> {
            if (i == EditorInfo.IME_ACTION_SEND)
            {
                addInputTxtToChat();
                return true;
            }
            return false;
        });
        mSendButton = contentView.findViewById(R.id.send_text);
        mSendButton.setOnClickListener(view -> {
            // just send the text to list of chat!
            addInputTxtToChat();
        });
        // register for the chat text event
        IntentFilter chatIntent = new IntentFilter(CHAT_BROADCAST);
        LocalBroadcastManager.getInstance(contentView.getContext()).registerReceiver(mChatBR, chatIntent);
    }

    @Override
    public void dismiss() {
        super.dismiss();
        // deregister from the event
        LocalBroadcastManager.getInstance(getContentView().getContext()).unregisterReceiver(mChatBR);
    }

    void addInputTxtToChat()
    {
        // get the input string from it
        String inputStr = mUserInput.getText().toString();
        // send the text message over bluetooth
        byte[] bytes = inputStr.getBytes(Charset.defaultCharset());
        BluetoothConn.write(bytes);
        // then send it to the receiver
        addTxtToChat("User: " + inputStr);
        mUserInput.getText().clear();
    }

    void addTxtToChat(String text) {
        // update the UI
        ChatViewRecycler chatAdapter = (ChatViewRecycler) mChatRecycler.getAdapter();
        chatAdapter.mListOfChatText.add(text);
        chatAdapter.notifyItemInserted(chatAdapter.mListOfChatText.size() - 1);
    }

    public static class ChatViewRecycler extends RecyclerView.Adapter<ChatViewRecycler.ViewHolder> {
        public ArrayList<String> mListOfChatText = new ArrayList<>();

        public ChatViewRecycler()
        {
        }

        @NonNull
        @Override
        public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
            // Create a new view, which defines the UI of the list item
            View view = LayoutInflater.from(parent.getContext())
                    .inflate(R.layout.bluetooth_chat_text, parent, false);
            return new ChatViewRecycler.ViewHolder(view);
        }

        @Override
        public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
            holder.mChatText.setText(mListOfChatText.get(position));
        }

        @Override
        public int getItemCount() {
            return mListOfChatText.size();
        }

        // meant for the chat's text!
        class ViewHolder extends RecyclerView.ViewHolder {
            public TextView mChatText;

            public ViewHolder(@NonNull View itemView) {
                super(itemView);
                mChatText =  itemView.findViewById(R.id.chat_text);
            }
        }
    }
}
